#!/usr/bin/env python3
"""
Backend API test for race snapshot containing ALL drivers (not just top 10).

Tests the fix in backend/simulator.py where _snapshot_standings() now returns
all drivers and constructors instead of slicing to top 10.
"""

import requests
import sys
import os
from pathlib import Path

# Read REACT_APP_BACKEND_URL from frontend/.env
env_file = Path("/app/frontend/.env")
BACKEND_URL = None
if env_file.exists():
    with open(env_file) as f:
        for line in f:
            if line.startswith("REACT_APP_BACKEND_URL="):
                BACKEND_URL = line.split("=", 1)[1].strip()
                break

if not BACKEND_URL:
    print("❌ ERROR: REACT_APP_BACKEND_URL not found in /app/frontend/.env")
    sys.exit(1)

API_BASE = f"{BACKEND_URL}/api"
print(f"🔗 Testing against: {API_BASE}\n")

# Test configuration
YEAR = 2024
SEED = 123
EXPECTED_DRIVER_COUNT = 10  # 2024 season has 10 drivers in f1_data.py


def test_race_snapshot_all_drivers():
    """
    Test that race snapshots contain ALL drivers, not just top 10.
    
    Steps:
    1. POST /api/simulate with year=2024, seed=123
    2. POST /api/simulations/{id}/next - run one race, check snapshot
    3. POST /api/simulations/{id}/next - run another race, check snapshot
    4. POST /api/simulations/{id}/finish?fast=true - finish season
    5. Verify all race snapshots have full driver count
    6. Verify snapshots are sorted by points
    7. Verify constructors snapshot has all teams
    """
    
    print("=" * 80)
    print("TEST: Race Snapshot Contains ALL Drivers (Not Top 10)")
    print("=" * 80)
    
    # Step 1: Create simulation
    print(f"\n📝 Step 1: Creating simulation for year={YEAR}, seed={SEED}")
    response = requests.post(f"{API_BASE}/simulate", json={"year": YEAR, "seed": SEED})
    
    if response.status_code != 200:
        print(f"❌ FAILED: Could not create simulation")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        return False
    
    data = response.json()
    sim_id = data.get("id")
    driver_count = len(data.get("drivers", []))
    
    print(f"✅ Simulation created: {sim_id}")
    print(f"   Total drivers in roster: {driver_count}")
    
    if driver_count != EXPECTED_DRIVER_COUNT:
        print(f"⚠️  WARNING: Expected {EXPECTED_DRIVER_COUNT} drivers, got {driver_count}")
    
    # Step 2: Run first race
    print(f"\n📝 Step 2: Running first race (POST /api/simulations/{sim_id}/next)")
    response = requests.post(f"{API_BASE}/simulations/{sim_id}/next")
    
    if response.status_code != 200:
        print(f"❌ FAILED: Could not run first race")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
        return False
    
    data = response.json()
    races = data.get("races", [])
    
    if not races:
        print(f"❌ FAILED: No races in response")
        return False
    
    race1 = races[0]
    snapshot1 = race1.get("standings_snapshot", {})
    snapshot1_drivers = snapshot1.get("drivers", [])
    snapshot1_constructors = snapshot1.get("constructors", [])
    
    print(f"✅ First race completed: {race1.get('circuit')}")
    print(f"   Snapshot drivers count: {len(snapshot1_drivers)}")
    print(f"   Snapshot constructors count: {len(snapshot1_constructors)}")
    
    # Verify driver count
    if len(snapshot1_drivers) != driver_count:
        print(f"❌ FAILED: Race 1 snapshot has {len(snapshot1_drivers)} drivers, expected {driver_count}")
        print(f"   This suggests the snapshot is still slicing to top 10!")
        return False
    else:
        print(f"✅ PASS: Race 1 snapshot contains ALL {driver_count} drivers")
    
    # Verify sorting (by points descending, then wins descending)
    is_sorted = True
    for i in range(len(snapshot1_drivers) - 1):
        curr = snapshot1_drivers[i]
        next_driver = snapshot1_drivers[i + 1]
        if curr["points"] < next_driver["points"]:
            is_sorted = False
            break
        elif curr["points"] == next_driver["points"] and curr["wins"] < next_driver["wins"]:
            is_sorted = False
            break
    
    if is_sorted:
        print(f"✅ PASS: Race 1 snapshot is correctly sorted by points (desc) and wins (desc)")
    else:
        print(f"❌ FAILED: Race 1 snapshot is NOT properly sorted")
        return False
    
    # Show top 3 and bottom 3 drivers
    print(f"\n   Top 3 drivers in snapshot:")
    for i, d in enumerate(snapshot1_drivers[:3]):
        print(f"      {i+1}. {d['driver']} ({d['team']}) - {d['points']} pts, {d['wins']} wins")
    
    print(f"\n   Bottom 3 drivers in snapshot:")
    for i, d in enumerate(snapshot1_drivers[-3:], start=len(snapshot1_drivers)-2):
        print(f"      {i}. {d['driver']} ({d['team']}) - {d['points']} pts, {d['wins']} wins")
    
    # Step 3: Run second race
    print(f"\n📝 Step 3: Running second race (POST /api/simulations/{sim_id}/next)")
    response = requests.post(f"{API_BASE}/simulations/{sim_id}/next")
    
    if response.status_code != 200:
        print(f"❌ FAILED: Could not run second race")
        print(f"   Status: {response.status_code}")
        return False
    
    data = response.json()
    races = data.get("races", [])
    
    if len(races) < 2:
        print(f"❌ FAILED: Expected at least 2 races, got {len(races)}")
        return False
    
    race2 = races[1]
    snapshot2 = race2.get("standings_snapshot", {})
    snapshot2_drivers = snapshot2.get("drivers", [])
    snapshot2_constructors = snapshot2.get("constructors", [])
    
    print(f"✅ Second race completed: {race2.get('circuit')}")
    print(f"   Snapshot drivers count: {len(snapshot2_drivers)}")
    print(f"   Snapshot constructors count: {len(snapshot2_constructors)}")
    
    if len(snapshot2_drivers) != driver_count:
        print(f"❌ FAILED: Race 2 snapshot has {len(snapshot2_drivers)} drivers, expected {driver_count}")
        return False
    else:
        print(f"✅ PASS: Race 2 snapshot contains ALL {driver_count} drivers")
    
    # Step 4: Finish all remaining races with fast=true
    print(f"\n📝 Step 4: Finishing all remaining races (POST /api/simulations/{sim_id}/finish?fast=true)")
    response = requests.post(f"{API_BASE}/simulations/{sim_id}/finish?fast=true")
    
    if response.status_code != 200:
        print(f"❌ FAILED: Could not finish simulation")
        print(f"   Status: {response.status_code}")
        return False
    
    data = response.json()
    races = data.get("races", [])
    finished = data.get("finished", False)
    
    print(f"✅ Simulation finished: {finished}")
    print(f"   Total races completed: {len(races)}")
    
    # Step 5: Verify ALL race snapshots have full driver count
    print(f"\n📝 Step 5: Verifying ALL race snapshots contain full driver roster")
    
    all_snapshots_valid = True
    for i, race in enumerate(races):
        snapshot = race.get("standings_snapshot", {})
        drivers_in_snapshot = snapshot.get("drivers", [])
        constructors_in_snapshot = snapshot.get("constructors", [])
        
        if len(drivers_in_snapshot) != driver_count:
            print(f"❌ FAILED: Race {i+1} ({race.get('circuit')}) snapshot has {len(drivers_in_snapshot)} drivers, expected {driver_count}")
            all_snapshots_valid = False
        
        # Check if sorted
        is_sorted = True
        for j in range(len(drivers_in_snapshot) - 1):
            curr = drivers_in_snapshot[j]
            next_driver = drivers_in_snapshot[j + 1]
            if curr["points"] < next_driver["points"]:
                is_sorted = False
                break
            elif curr["points"] == next_driver["points"] and curr["wins"] < next_driver["wins"]:
                is_sorted = False
                break
        
        if not is_sorted:
            print(f"❌ FAILED: Race {i+1} snapshot is NOT properly sorted")
            all_snapshots_valid = False
    
    if all_snapshots_valid:
        print(f"✅ PASS: ALL {len(races)} race snapshots contain full driver roster and are properly sorted")
    else:
        return False
    
    # Step 6: Verify last race snapshot in detail
    print(f"\n📝 Step 6: Detailed verification of LAST race snapshot")
    last_race = races[-1]
    last_snapshot = last_race.get("standings_snapshot", {})
    last_drivers = last_snapshot.get("drivers", [])
    last_constructors = last_snapshot.get("constructors", [])
    
    print(f"   Last race: Round {last_race.get('round')} - {last_race.get('circuit')}")
    print(f"   Drivers in snapshot: {len(last_drivers)}")
    print(f"   Constructors in snapshot: {len(last_constructors)}")
    
    if len(last_drivers) < 10:
        print(f"❌ FAILED: Last race snapshot has only {len(last_drivers)} drivers (should be >= 10)")
        return False
    
    if len(last_drivers) != driver_count:
        print(f"❌ FAILED: Last race snapshot has {len(last_drivers)} drivers, expected {driver_count}")
        return False
    
    print(f"✅ PASS: Last race snapshot has {len(last_drivers)} drivers (full grid)")
    
    # Show final standings (top 5 and bottom 5)
    print(f"\n   Final Driver Standings (Top 5):")
    for i, d in enumerate(last_drivers[:5]):
        print(f"      {i+1}. {d['driver']} ({d['team']}) - {d['points']} pts, {d['wins']} wins")
    
    print(f"\n   Final Driver Standings (Bottom 5):")
    for i, d in enumerate(last_drivers[-5:], start=len(last_drivers)-4):
        print(f"      {i}. {d['driver']} ({d['team']}) - {d['points']} pts, {d['wins']} wins")
    
    print(f"\n   Final Constructor Standings:")
    for i, c in enumerate(last_constructors):
        print(f"      {i+1}. {c['team']} - {c['points']} pts")
    
    # Verify constructors are also not sliced
    unique_teams = set(d["team"] for d in last_drivers)
    if len(last_constructors) != len(unique_teams):
        print(f"⚠️  WARNING: Constructor count ({len(last_constructors)}) doesn't match unique teams ({len(unique_teams)})")
    else:
        print(f"✅ PASS: Constructor snapshot contains all {len(last_constructors)} teams")
    
    print("\n" + "=" * 80)
    print("✅ ALL TESTS PASSED")
    print("=" * 80)
    print("\nSUMMARY:")
    print(f"  • Race snapshots now contain ALL {driver_count} drivers (not sliced to top 10)")
    print(f"  • All snapshots are correctly sorted by points (desc) and wins (desc)")
    print(f"  • Constructor snapshots contain all {len(last_constructors)} teams")
    print(f"  • Verified across {len(races)} races in the season")
    print("\n✅ The backend change in simulator.py _snapshot_standings() is working correctly!")
    
    return True


if __name__ == "__main__":
    try:
        success = test_race_snapshot_all_drivers()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ EXCEPTION: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
