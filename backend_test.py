#!/usr/bin/env python3
"""
Backend API tests for F1 simulator after data expansion.
Tests that seasons 2010-2025 have 20 drivers (10 teams x 2 drivers).
"""
import requests
import json
import sys
import time

# Backend URL from frontend/.env
BASE_URL = "https://track-action-hub.preview.emergentagent.com/api"

def test_season_detail(year, expected_driver_count):
    """Test GET /api/seasons/{year} returns expected number of drivers."""
    print(f"\n{'='*80}")
    print(f"TEST: GET /api/seasons/{year}")
    print(f"Expected driver count: {expected_driver_count}")
    print(f"{'='*80}")
    
    url = f"{BASE_URL}/seasons/{year}"
    try:
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ FAILED: Expected 200, got {response.status_code}")
            print(f"Response: {response.text}")
            return False
        
        data = response.json()
        driver_count = len(data.get("drivers", []))
        
        print(f"Actual driver count: {driver_count}")
        print(f"Champion: {data.get('champion')}")
        print(f"Champion Team: {data.get('champion_team')}")
        print(f"Constructors Champion: {data.get('constructors_champion')}")
        print(f"Number of races: {data.get('num_races')}")
        
        # List all drivers and teams
        print(f"\nDrivers and Teams:")
        teams = set()
        for i, driver in enumerate(data.get("drivers", []), 1):
            print(f"  {i:2d}. {driver['name']:30s} - {driver['team']:20s} (Rating: {driver['rating']})")
            teams.add(driver['team'])
        
        print(f"\nUnique teams ({len(teams)}): {', '.join(sorted(teams))}")
        
        if driver_count == expected_driver_count:
            print(f"✅ PASSED: Season {year} has {driver_count} drivers")
            return True
        else:
            print(f"❌ FAILED: Expected {expected_driver_count} drivers, got {driver_count}")
            return False
            
    except Exception as e:
        print(f"❌ FAILED: Exception occurred: {e}")
        return False


def test_simulation_with_20_drivers():
    """Test POST /api/simulate with year 2025, seed 42, then run next race."""
    print(f"\n{'='*80}")
    print(f"TEST: POST /api/simulate (year=2025, seed=42) + next race")
    print(f"{'='*80}")
    
    # Create simulation
    url = f"{BASE_URL}/simulate"
    payload = {"year": 2025, "seed": 42}
    
    try:
        print(f"Creating simulation with payload: {payload}")
        response = requests.post(url, json=payload, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ FAILED: Expected 200, got {response.status_code}")
            print(f"Response: {response.text}")
            return False
        
        sim_data = response.json()
        sim_id = sim_data.get("id")
        print(f"✅ Simulation created with ID: {sim_id}")
        print(f"Year: {sim_data.get('year')}")
        print(f"Seed: {sim_data.get('seed')}")
        print(f"Total races: {sim_data.get('total_races')}")
        print(f"Current race: {sim_data.get('current_race')}")
        
        # Run first race
        print(f"\nRunning first race...")
        next_url = f"{BASE_URL}/simulations/{sim_id}/next"
        response = requests.post(next_url, timeout=30)
        print(f"Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ FAILED: Expected 200, got {response.status_code}")
            print(f"Response: {response.text}")
            return False
        
        race_data = response.json()
        races = race_data.get("races", [])
        
        if not races:
            print(f"❌ FAILED: No races found in response")
            return False
        
        last_race = races[-1]
        snapshot = last_race.get("standings_snapshot", {})
        drivers_snapshot = snapshot.get("drivers", [])
        constructors_snapshot = snapshot.get("constructors", [])
        
        print(f"\n✅ Race {last_race.get('round')} completed at {last_race.get('circuit')}")
        print(f"Drivers in standings_snapshot: {len(drivers_snapshot)}")
        print(f"Constructors in standings_snapshot: {len(constructors_snapshot)}")
        
        # Verify 20 drivers and 10 constructors
        if len(drivers_snapshot) != 20:
            print(f"❌ FAILED: Expected 20 drivers in snapshot, got {len(drivers_snapshot)}")
            return False
        
        if len(constructors_snapshot) != 10:
            print(f"❌ FAILED: Expected 10 constructors in snapshot, got {len(constructors_snapshot)}")
            return False
        
        print(f"\nTop 10 drivers after race 1:")
        for i, driver in enumerate(drivers_snapshot[:10], 1):
            print(f"  {i:2d}. {driver['driver']:30s} - {driver['team']:20s} (Points: {driver['points']}, Wins: {driver['wins']})")
        
        print(f"\nAll constructors after race 1:")
        for i, constructor in enumerate(constructors_snapshot, 1):
            print(f"  {i:2d}. {constructor['team']:20s} (Points: {constructor['points']})")
        
        print(f"\n✅ PASSED: Simulation has 20 drivers and 10 constructors in snapshot")
        return sim_id
        
    except Exception as e:
        print(f"❌ FAILED: Exception occurred: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_run_more_races(sim_id, num_races=3):
    """Run additional races to confirm simulation keeps working."""
    print(f"\n{'='*80}")
    print(f"TEST: Run {num_races} more races in simulation {sim_id}")
    print(f"{'='*80}")
    
    try:
        for i in range(num_races):
            print(f"\nRunning race {i+2}...")
            url = f"{BASE_URL}/simulations/{sim_id}/next"
            response = requests.post(url, timeout=30)
            print(f"Status: {response.status_code}")
            
            if response.status_code != 200:
                print(f"❌ FAILED: Expected 200, got {response.status_code}")
                print(f"Response: {response.text}")
                return False
            
            race_data = response.json()
            races = race_data.get("races", [])
            last_race = races[-1]
            snapshot = last_race.get("standings_snapshot", {})
            drivers_snapshot = snapshot.get("drivers", [])
            constructors_snapshot = snapshot.get("constructors", [])
            
            print(f"✅ Race {last_race.get('round')} completed at {last_race.get('circuit')}")
            print(f"   Drivers in snapshot: {len(drivers_snapshot)}")
            print(f"   Constructors in snapshot: {len(constructors_snapshot)}")
            
            if len(drivers_snapshot) != 20:
                print(f"❌ FAILED: Expected 20 drivers, got {len(drivers_snapshot)}")
                return False
            
            if len(constructors_snapshot) != 10:
                print(f"❌ FAILED: Expected 10 constructors, got {len(constructors_snapshot)}")
                return False
            
            # Show top 3
            print(f"   Top 3: ", end="")
            for j, driver in enumerate(drivers_snapshot[:3], 1):
                print(f"{j}. {driver['driver']} ({driver['points']}pts)", end="  ")
            print()
        
        print(f"\n✅ PASSED: All {num_races} races completed successfully with 20 drivers")
        return True
        
    except Exception as e:
        print(f"❌ FAILED: Exception occurred: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_champion_verification(year=2025):
    """Verify the champion and champion_team for a season."""
    print(f"\n{'='*80}")
    print(f"TEST: Verify champion for {year}")
    print(f"{'='*80}")
    
    url = f"{BASE_URL}/seasons/{year}"
    try:
        response = requests.get(url, timeout=10)
        print(f"Status: {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ FAILED: Expected 200, got {response.status_code}")
            return False
        
        data = response.json()
        champion = data.get("champion")
        champion_team = data.get("champion_team")
        
        print(f"Champion: {champion}")
        print(f"Champion Team: {champion_team}")
        
        if year == 2025:
            if champion == "Lando Norris" and champion_team == "McLaren":
                print(f"✅ PASSED: 2025 champion is Lando Norris (McLaren)")
                return True
            else:
                print(f"❌ FAILED: Expected Lando Norris (McLaren), got {champion} ({champion_team})")
                return False
        
        return True
        
    except Exception as e:
        print(f"❌ FAILED: Exception occurred: {e}")
        return False


def test_teams_presence(years, expected_teams):
    """Verify that specific teams are present in given years."""
    print(f"\n{'='*80}")
    print(f"TEST: Verify teams presence in years {years}")
    print(f"Expected teams: {', '.join(expected_teams)}")
    print(f"{'='*80}")
    
    all_passed = True
    
    for year in years:
        url = f"{BASE_URL}/seasons/{year}"
        try:
            response = requests.get(url, timeout=10)
            if response.status_code != 200:
                print(f"❌ FAILED: Year {year} - Status {response.status_code}")
                all_passed = False
                continue
            
            data = response.json()
            drivers = data.get("drivers", [])
            teams = set(driver['team'] for driver in drivers)
            
            missing_teams = set(expected_teams) - teams
            
            if missing_teams:
                print(f"❌ FAILED: Year {year} - Missing teams: {', '.join(missing_teams)}")
                print(f"   Available teams: {', '.join(sorted(teams))}")
                all_passed = False
            else:
                print(f"✅ PASSED: Year {year} - All expected teams present")
                print(f"   Teams: {', '.join(sorted(teams))}")
        
        except Exception as e:
            print(f"❌ FAILED: Year {year} - Exception: {e}")
            all_passed = False
    
    return all_passed


def main():
    """Run all tests."""
    print("="*80)
    print("F1 BACKEND API TESTS - DATA EXPANSION VERIFICATION")
    print("="*80)
    print(f"Backend URL: {BASE_URL}")
    print("="*80)
    
    results = []
    
    # Test 1: GET /api/seasons/2025 → 20 drivers
    results.append(("2025 season (20 drivers)", test_season_detail(2025, 20)))
    
    # Test 2: GET /api/seasons/2024 → 20 drivers
    results.append(("2024 season (20 drivers)", test_season_detail(2024, 20)))
    
    # Test 3: GET /api/seasons/2023 → 20 drivers
    results.append(("2023 season (20 drivers)", test_season_detail(2023, 20)))
    
    # Test 4: GET /api/seasons/2022 → 20 drivers
    results.append(("2022 season (20 drivers)", test_season_detail(2022, 20)))
    
    # Test 5: GET /api/seasons/2021 → 20 drivers
    results.append(("2021 season (20 drivers)", test_season_detail(2021, 20)))
    
    # Test 6: GET /api/seasons/2020 → 20 drivers
    results.append(("2020 season (20 drivers)", test_season_detail(2020, 20)))
    
    # Test 7: GET /api/seasons/2015 → 20 drivers
    results.append(("2015 season (20 drivers)", test_season_detail(2015, 20)))
    
    # Test 8: GET /api/seasons/2010 → 20 drivers
    results.append(("2010 season (20 drivers)", test_season_detail(2010, 20)))
    
    # Test 9: GET /api/seasons/2000 → ~10 drivers (not expanded)
    results.append(("2000 season (~10 drivers)", test_season_detail(2000, 10)))
    
    # Test 10: POST /api/simulate + next race with 20 drivers
    sim_id = test_simulation_with_20_drivers()
    results.append(("Simulation with 20 drivers", bool(sim_id)))
    
    # Test 11: Run 3 more races
    if sim_id:
        results.append(("Run 3 more races", test_run_more_races(sim_id, 3)))
    else:
        results.append(("Run 3 more races", False))
    
    # Test 12: Verify 2025 champion
    results.append(("2025 champion verification", test_champion_verification(2025)))
    
    # Test 13: Verify teams presence
    expected_teams = ["Red Bull", "McLaren", "Ferrari", "Mercedes"]
    test_years = [2010, 2015, 2020, 2025]
    results.append(("Teams presence verification", test_teams_presence(test_years, expected_teams)))
    
    # Summary
    print("\n" + "="*80)
    print("TEST SUMMARY")
    print("="*80)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASSED" if result else "❌ FAILED"
        print(f"{status}: {test_name}")
    
    print("="*80)
    print(f"TOTAL: {passed}/{total} tests passed")
    print("="*80)
    
    return passed == total


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
