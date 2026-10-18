"""Orchestrates the full pipeline: generate sample data -> create schema -> stage -> warehouse."""

import generate_sample_data
import create_schema
import extract_load_staging
import transform_load_warehouse


def main():
    print("=== Step 1: Generate sample source data ===")
    generate_sample_data.main()

    print("\n=== Step 2: Create schema (staging + warehouse) ===")
    create_schema.main()

    print("\n=== Step 3: Extract & load into staging ===")
    extract_load_staging.main()

    print("\n=== Step 4: Transform & load into warehouse (star schema) ===")
    transform_load_warehouse.main()

    print("\nPipeline finished successfully.")


if __name__ == "__main__":
    main()
