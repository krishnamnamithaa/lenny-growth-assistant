import sys
import argparse
import logging
from app.db import init_db, SessionLocal
from app.rag.ingestion import run_ingestion_pipeline

def main():
    parser = argparse.ArgumentParser(description="Lenny Growth Assistant CLI")
    subparsers = parser.add_subparsers(dest="command", help="Available CLI commands")

    # Ingest subcommand
    ingest_parser = subparsers.add_parser("ingest", help="Ingest transcript files into pgvector")
    ingest_parser.add_argument(
        "--dir", "-d",
        default="data/transcripts",
        help="Path to transcripts directory (default: data/transcripts)"
    )
    ingest_parser.add_argument(
        "--db-url",
        default=None,
        help="Optional database URL override (e.g. sqlite:///lenny_dev.db for offline testing)"
    )

    args = parser.parse_args()

    if args.command == "ingest":
        print("\n==================================================")
        print("  Lenny Growth Assistant — Transcript Ingestion  ")
        print("==================================================\n")
        print(f"Source Directory: {args.dir}")

        custom_engine = None
        db_session = None
        if args.db_url:
            from sqlalchemy import create_engine
            from sqlalchemy.orm import sessionmaker
            print(f"Database URL     : {args.db_url}")
            custom_engine = create_engine(args.db_url, pool_pre_ping=True)
            init_db(db_engine=custom_engine)
            SessionCustom = sessionmaker(autocommit=False, autoflush=False, bind=custom_engine)
            db_session = SessionCustom()
        else:
            init_db()
            db_session = SessionLocal()

        print("\nProcessing transcripts...")
        stats = run_ingestion_pipeline(transcripts_dir=args.dir, db=db_session)
        db_session.close()


        print("\n--------------------------------------------------")
        print("Ingestion Completed Summary:")
        print(f"  Transcripts Found     : {stats['found']}")
        print(f"  Transcripts Processed : {stats['processed']}")
        print(f"  Chunks Created        : {stats['chunks_created']}")
        print(f"  Skipped (Invalid)     : {stats['skipped']}")
        print(f"  Errors                : {stats['errors']}")
        print("--------------------------------------------------\n")

        if stats["errors"] > 0:
            sys.exit(1)
        sys.exit(0)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
