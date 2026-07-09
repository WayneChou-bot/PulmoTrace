"""Regression tests for patient-level splitting — the most fatal pitfall.

These assert that no patient ever crosses train/val/test. This guard must never
regress: any Dice number in the project must be answerable with "yes, this was a
patient-level split".
"""
import numpy as np
import pytest

from cxrseg.splits import (
    Split,
    patient_level_split,
    assert_no_patient_leakage,
    nih_patient_id_from_filename,
)


def _make_dataset(n_patients=100, max_imgs=5, seed=0):
    """Each patient has 1..max_imgs images. Returns (patient_ids, filenames)."""
    rng = np.random.default_rng(seed)
    patient_ids, filenames = [], []
    for p in range(n_patients):
        pid = f"{p:08d}"
        n_imgs = int(rng.integers(1, max_imgs + 1))
        for k in range(n_imgs):
            patient_ids.append(pid)
            filenames.append(f"{pid}_{k:03d}.png")
    return patient_ids, filenames


def test_no_patient_crosses_splits():
    patient_ids, _ = _make_dataset()
    split = patient_level_split(patient_ids, test_size=0.2, val_size=0.1, seed=42)
    # The core guarantee — must hold.
    assert_no_patient_leakage(patient_ids, split)


def test_all_images_of_a_patient_stay_together():
    patient_ids, _ = _make_dataset()
    split = patient_level_split(patient_ids, seed=7)
    pid_arr = np.asarray(patient_ids)
    members = {
        "train": set(pid_arr[split.train]),
        "val": set(pid_arr[split.val]),
        "test": set(pid_arr[split.test]),
    }
    # every image's patient must be in exactly one split's member set
    for name, idxs in (("train", split.train), ("val", split.val), ("test", split.test)):
        for i in idxs:
            assert patient_ids[i] in members[name]


def test_covers_every_image_exactly_once():
    patient_ids, _ = _make_dataset()
    split = patient_level_split(patient_ids)
    all_idx = np.concatenate([split.train, split.val, split.test])
    assert sorted(all_idx.tolist()) == list(range(len(patient_ids)))


def test_reproducible_with_seed():
    patient_ids, _ = _make_dataset()
    a = patient_level_split(patient_ids, seed=123)
    b = patient_level_split(patient_ids, seed=123)
    assert np.array_equal(a.train, b.train)
    assert np.array_equal(a.val, b.val)
    assert np.array_equal(a.test, b.test)


def test_different_seed_changes_split():
    patient_ids, _ = _make_dataset()
    a = patient_level_split(patient_ids, seed=1)
    b = patient_level_split(patient_ids, seed=2)
    assert not np.array_equal(a.test, b.test)


def test_patient_level_proportions_roughly_hold():
    patient_ids, _ = _make_dataset(n_patients=1000)
    split = patient_level_split(patient_ids, test_size=0.2, val_size=0.1, seed=42)
    pid_arr = np.asarray(patient_ids)
    n_pat = len(set(patient_ids))
    assert abs(len(set(pid_arr[split.test])) / n_pat - 0.2) < 0.03
    assert abs(len(set(pid_arr[split.val])) / n_pat - 0.1) < 0.03


def test_leakage_assertion_catches_a_deliberately_leaky_split():
    # Same patient forced into both train and test → guard must fire.
    patient_ids = ["A", "A", "B", "B", "C", "C"]
    leaky = Split(train=np.array([0, 2]), val=np.array([4]), test=np.array([1, 3, 5]))
    # patient A is in train (idx0) and test (idx1)
    with pytest.raises(AssertionError):
        assert_no_patient_leakage(patient_ids, leaky)


def test_empty_input():
    split = patient_level_split([])
    assert split.sizes() == (0, 0, 0)


def test_invalid_sizes_raise():
    with pytest.raises(ValueError):
        patient_level_split(["A", "B"], test_size=0.7, val_size=0.5)


def test_nih_patient_id_parsing():
    assert nih_patient_id_from_filename("00000001_000.png") == "00000001"
    assert nih_patient_id_from_filename("00013118_045.png") == "00013118"
    assert nih_patient_id_from_filename("/data/images/00000042_007.png") == "00000042"
    # windows-style path
    assert nih_patient_id_from_filename(r"C:\imgs\00000099_001.png") == "00000099"


def test_split_by_image_would_leak_but_patient_split_does_not():
    """Sanity contrast: a naive image-level shuffle leaks; ours does not."""
    patient_ids, _ = _make_dataset(n_patients=50, max_imgs=6, seed=3)
    n = len(patient_ids)
    rng = np.random.default_rng(0)
    perm = rng.permutation(n)
    naive_test = set(np.asarray(patient_ids)[perm[: n // 5]])
    naive_train = set(np.asarray(patient_ids)[perm[n // 5 :]])
    # naive image-level split almost certainly leaks patients
    assert not naive_test.isdisjoint(naive_train)
    # ours does not
    split = patient_level_split(patient_ids, seed=42)
    assert_no_patient_leakage(patient_ids, split)
