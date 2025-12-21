from app.polistock_app import run_polistock

if __name__ == "__main__":
    print("Welcome to Polistock - Congressional Activity Tracker")
    print("=" * 60)
    
    try:
        official = run_polistock()
        print("\n✅ Data collection complete!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()