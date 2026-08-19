from pathlib import Path
import pandas as pd

DATA_PROCESSED_DIR = Path(__file__).parent.parent / "data" / "processed"


def test_numeric_columns_are_numeric():
    df = pd.read_csv(DATA_PROCESSED_DIR / "video_data.csv")

    assert pd.api.types.is_numeric_dtype(df["view_count"])
    assert pd.api.types.is_numeric_dtype(df["like_count"])
    assert pd.api.types.is_numeric_dtype(df["comment_count"])

def test_no_duplicate_video_ids():
    df = pd.read_csv(DATA_PROCESSED_DIR / "video_data.csv")
    assert df["video_id"].is_unique

def test_required_fields_not_null():
    df = pd.read_csv(DATA_PROCESSED_DIR / "video_data.csv")
    assert df["title"].notna().all()
    assert df["published_at"].notna().all()
    assert df["view_count"].notna().all()

def test_expected_channels_present():
    df = pd.read_csv(DATA_PROCESSED_DIR / "video_data.csv")
    expected_channels = {
        "Cocomelon - Nursery Rhymes",
        "Ryan's World",
        "Baby Shark - Pinkfong Kids' Songs & Stories",
        "Blippi - Educational Videos for Kids",
        "Alan Becker",
        "TomSka",
        "Netflix",
        "Warner Bros.",
    }
    assert set(df["channel_name"].unique()) == expected_channels