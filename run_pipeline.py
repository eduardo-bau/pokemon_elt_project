#!/usr/bin/env python3
"""
Pokemon ELT Pipeline Orchestrator
Runs the complete Extract, Load, Transform pipeline
"""
import subprocess
import sys
from pathlib import Path
import time


class PipelineOrchestrator:
    """Orchestrate the ELT pipeline"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.extract_script = self.project_root / "extract" / "extract_pokemon.py"
        self.dbt_project = self.project_root / "transform" / "pokemon_dbt"
    
    def run_extract(self):
        """Run extraction phase"""
        print("\n" + "="*70)
        print("PHASE 1: EXTRACT")
        print("="*70)
        
        try:
            result = subprocess.run(
                [sys.executable, str(self.extract_script)],
                check=True,
                capture_output=True,
                text=True
            )
            print(result.stdout)
            print("✓ Extract phase completed successfully")
            return True
        except subprocess.CalledProcessError as e:
            print(f"✗ Extract phase failed: {e}")
            print(e.stdout)
            print(e.stderr)
            return False
    
    def run_transform(self):
        """Run transformation phase with dbt"""
        print("\n" + "="*70)
        print("PHASE 2: TRANSFORM (dbt)")
        print("="*70)
        
        try:
            # Run dbt debug to check connection
            print("\nChecking dbt connection...")
            subprocess.run(
                ["dbt", "debug", "--project-dir", str(self.dbt_project)],
                check=True
            )
            
            # Run dbt deps (if you have packages)
            print("\nInstalling dbt dependencies...")
            subprocess.run(
                ["dbt", "deps", "--project-dir", str(self.dbt_project)],
                check=False  # Don't fail if no packages
            )
            
            # Run dbt models
            print("\nRunning dbt models...")
            subprocess.run(
                ["dbt", "run", "--project-dir", str(self.dbt_project)],
                check=True
            )
            
            # Run dbt tests
            print("\nRunning dbt tests...")
            subprocess.run(
                ["dbt", "test", "--project-dir", str(self.dbt_project)],
                check=True
            )
            
            print("\n✓ Transform phase completed successfully")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"\n✗ Transform phase failed: {e}")
            return False
    
    def generate_docs(self):
        """Generate dbt documentation"""
        print("\n" + "="*70)
        print("GENERATING DOCUMENTATION")
        print("="*70)
        
        try:
            # Generate documentation
            subprocess.run(
                ["dbt", "docs", "generate", "--project-dir", str(self.dbt_project)],
                check=True
            )
            print("\n✓ Documentation generated successfully")
            print(f"  Run 'dbt docs serve --project-dir {self.dbt_project}' to view")
            return True
            
        except subprocess.CalledProcessError as e:
            print(f"\n✗ Documentation generation failed: {e}")
            return False
    
    def run_pipeline(self, skip_extract=False, skip_transform=False):
        """Run the complete pipeline"""
        print("\n" + "="*70)
        print("POKEMON ELT PIPELINE")
        print("="*70)
        print(f"Start time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        start_time = time.time()
        
        # Extract
        if not skip_extract:
            if not self.run_extract():
                print("\n✗ Pipeline failed at Extract phase")
                return False
        else:
            print("\n⊘ Skipping Extract phase")
        
        # Transform
        if not skip_transform:
            if not self.run_transform():
                print("\n✗ Pipeline failed at Transform phase")
                return False
        else:
            print("\n⊘ Skipping Transform phase")
        
        # Generate docs
        self.generate_docs()
        
        # Summary
        duration = time.time() - start_time
        print("\n" + "="*70)
        print("PIPELINE COMPLETED SUCCESSFULLY")
        print("="*70)
        print(f"Duration: {duration:.2f} seconds")
        print(f"End time: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        
        return True


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Run Pokemon ELT Pipeline")
    parser.add_argument("--skip-extract", action="store_true", 
                       help="Skip extraction phase")
    parser.add_argument("--skip-transform", action="store_true",
                       help="Skip transformation phase")
    
    args = parser.parse_args()
    
    orchestrator = PipelineOrchestrator()
    success = orchestrator.run_pipeline(
        skip_extract=args.skip_extract,
        skip_transform=args.skip_transform
    )
    
    sys.exit(0 if success else 1)
