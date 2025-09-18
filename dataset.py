import csv
import random
import datetime as dt
import numpy as np
from pathlib import Path

# -----------------------------
# CONFIGURABLE SETTINGS
# -----------------------------
NUM_TRAINS = 25          # fleet size
NUM_DAYS   = 30          # number of days
OUTPUT_CSV = Path("kochi_metro_synthetic1.csv")

DEPOTS = ["Aluva", "M.G.Road"]

# -----------------------------
# HELPER FUNCTIONS
# -----------------------------
def bool_with_prob(p):
    return random.random() < p

def gen_row(date: dt.date, train_id: str, depot: str) -> dict:
    """Generate one synthetic nightly record for a single train."""

    # --- Odometer & wear ---
    odometer_total = 400_000 + random.gauss(0, 20_000)
    km_last_30d    = max(0, random.gauss(1000, 300))
    km_last_7d     = max(0, random.gauss(250, 60))
    wear_index     = min(1.0, 0.2 + (odometer_total - 300_000)/1e6
                         + 0.3*(km_last_30d/2000))

    # --- Fitness certificates ---
    rs_expiry  = date + dt.timedelta(days=random.randint(-2, 30))
    sig_expiry = date + dt.timedelta(days=random.randint(-2, 30))
    tel_expiry = date + dt.timedelta(days=random.randint(-2, 30))

    fitness_rs_valid  = rs_expiry > date
    fitness_sig_valid = sig_expiry > date
    fitness_tel_valid = tel_expiry > date
    fitness_all_valid = all([fitness_rs_valid, fitness_sig_valid, fitness_tel_valid])

    # --- Job-card / Maximo ---
    open_jobs = np.random.poisson(0.4)
    critical_job = open_jobs > 2 and bool_with_prob(0.4)
    job_card_last_update = date - dt.timedelta(hours=random.randint(0, 48))

    # --- Branding ---
    branding_contract = random.choice([None, f"BR-{random.randint(1,99):03d}"])
    branding_min_hours = random.choice([0, 5, 8, 10]) if branding_contract else 0
    branding_curr_hours = random.uniform(0, 12) if branding_contract else 0
    branding_penalty = random.uniform(1000, 5000) if branding_contract else 0

    # --- Cleaning & detailing ---
    cleaning_required = bool_with_prob(0.15)
    cleaning_slot_booked = cleaning_required and bool_with_prob(0.75)
    cleaning_slot_time = (f"{random.randint(21,23)}:00-"
                          f"{random.randint(0,3)+0:02d}:00") if cleaning_slot_booked else ""

    # --- Stabling geometry ---
    home_bay = random.randint(1, 10)
    bay_proximity_score = round(random.uniform(0,1), 2)
    shunting_moves_needed = random.randint(0, 5)

    # --- Other ops signals ---
    crew_available = bool_with_prob(0.95)
    hvac_temp      = round(random.uniform(20, 30), 1)
    telemetry_last_seen = date - dt.timedelta(hours=random.randint(0, 12))
    manual_override = bool_with_prob(0.05)
    whatsapp_updates = np.random.poisson(0.3)

    # --- Derived constraints ---
    violates_fitness = not fitness_all_valid
    violates_critical_job = critical_job

    # --- Rank score / decision ---
    score = 0.0
    if violates_fitness: score -= 10
    if violates_critical_job: score -= 8
    if cleaning_required and not cleaning_slot_booked: score -= 1
    score -= abs(km_last_30d - 900) / 1500
    score -= shunting_moves_needed * 0.1
    if manual_override: score += 100

    if manual_override:
        decision = "enter_service"
    elif violates_fitness or violates_critical_job:
        decision = "hold_in_ibl"
    elif score < -2:
        decision = "standby"
    else:
        decision = "enter_service"

    # --- Possible next-day withdrawal outcome ---
    fail_prob = 0.02 + 0.05*wear_index + 0.1*int(violates_fitness)
    unscheduled_withdrawal = bool_with_prob(min(fail_prob, 0.9))

    # -----------------------------
    # Probability of use
    # -----------------------------
    prob_use = 0.9
    if violates_fitness: prob_use -= 0.4
    if violates_critical_job: prob_use -= 0.3
    if cleaning_required and not cleaning_slot_booked: prob_use -= 0.1
    prob_use -= 0.2 * wear_index
    prob_use += 0.05 if manual_override else 0
    prob_use = max(0.0, min(1.0, prob_use))

    # Recommendation
    if prob_use >= 0.8:
        recommendation = "Ready for service"
    elif prob_use >= 0.5:
        recommendation = "Schedule maintenance soon"
    else:
        recommendation = "Hold for immediate inspection"

    # Final score (weighted for more realistic planning)
    # rank_score is already approx -15 to +100; we combine with probability*100
    final_score = round(0.7 * score + 0.3 * (prob_use * 100), 2)

    return {
        "date": date.isoformat(),
        "depot": depot,
        "train_id": train_id,
        "rake_status_current": random.choice(["in_service","stabled","in_ibl"]),
        "fitness_rolling_stock_expiry": rs_expiry.isoformat(),
        "fitness_signalling_expiry": sig_expiry.isoformat(),
        "fitness_telecom_expiry": tel_expiry.isoformat(),
        "fitness_all_valid": fitness_all_valid,
        "open_job_cards_count": int(open_jobs),
        "critical_job_card_flag": critical_job,
        "job_card_last_update": job_card_last_update.isoformat(),
        "branding_contract_id": branding_contract or "",
        "branding_min_exposure_hours": branding_min_hours,
        "branding_current_exposure_hours_last_7d": round(branding_curr_hours,1),
        "branding_penalty_if_missed": round(branding_penalty,2),
        "odometer_total_km": round(odometer_total,1),
        "km_last_7d": round(km_last_7d,1),
        "km_last_30d": round(km_last_30d,1),
        "wear_index": round(wear_index,3),
        "cleaning_required": cleaning_required,
        "cleaning_slot_booked": cleaning_slot_booked,
        "cleaning_slot_time": cleaning_slot_time,
        "home_bay": home_bay,
        "bay_proximity_score": bay_proximity_score,
        "shunting_moves_needed": shunting_moves_needed,
        "crew_available_flag": crew_available,
        "iot_temp_hvac_status": hvac_temp,
        "telemetry_last_seen": telemetry_last_seen.isoformat(),
        "manual_override_flag": manual_override,
        "whatsapp_update_count": int(whatsapp_updates),
        "violates_mandatory_fitness": violates_fitness,
        "violates_critical_job": violates_critical_job,
        "expected_shunting_energy_cost": round(shunting_moves_needed * 0.5, 2),
        "rank_score": round(score,2),
        "induction_decision": decision,
        "unscheduled_withdrawal_within_24h": unscheduled_withdrawal,
        "probability_of_use": round(prob_use,3),
        "recommendation": recommendation,
        # placeholders to fill after ranking pass
        "probability_rank": None,
        "final_score": final_score
    }

# -----------------------------
# MAIN GENERATION LOOP
# -----------------------------
def main():
    start_date = dt.date.today() - dt.timedelta(days=NUM_DAYS)
    rows = []
    for d in range(NUM_DAYS):
        date = start_date + dt.timedelta(days=d)
        day_rows = []
        for t in range(1, NUM_TRAINS + 1):
            train_id = f"TS{t:03d}"
            depot = random.choice(DEPOTS)
            day_rows.append(gen_row(date, train_id, depot))

        # Rank trains by probability_of_use for this day
        day_rows.sort(key=lambda r: r["probability_of_use"], reverse=True)
        for rank, r in enumerate(day_rows, start=1):
            r["probability_rank"] = rank

        rows.extend(day_rows)

    fieldnames = list(rows[0].keys())
    with OUTPUT_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Generated {len(rows)} rows → {OUTPUT_CSV.resolve()}")

if __name__ == "_main_":
    main()