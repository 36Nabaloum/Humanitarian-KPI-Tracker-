import csv
import random
from datetime import date, timedelta

random.seed(42)

countries = ["Burkina Faso", "Mali", "Niger", "Chad", "Senegal"]
regions = {
    "Burkina Faso": ["Centre", "Sahel", "Nord", "Est", "Cascades"],
    "Mali":         ["Bamako", "Mopti", "Gao", "Tombouctou", "Segou"],
    "Niger":        ["Niamey", "Zinder", "Maradi", "Agadez", "Diffa"],
    "Chad":         ["N'Djamena", "Lac", "Ouaddai", "Borkou", "Kanem"],
    "Senegal":      ["Dakar", "Thiès", "Saint-Louis", "Ziguinchor", "Louga"],
}
sectors = ["Nutrition", "WASH", "Shelter", "Protection", "Health", "Food Security", "Education"]
donors  = ["USAID", "UNICEF", "OCHA", "NORAD", "BHA", "GFFO", "EU"]
org_types = ["INGO", "NGO", "UN Agency", "Government"]
orgs = {
    "INGO":      ["IRC", "Oxfam", "MSF", "Save the Children", "ACF"],
    "NGO":       ["SPONG", "CREDO", "AMADE", "AFRIQUE ESPOIR", "CISV"],
    "UN Agency": ["UNICEF", "WFP", "UNHCR", "WHO", "FAO"],
    "Government":["DREP", "DNDS", "MASF", "MSHP", "MENA"],
}
indicators = {
    "Nutrition":     ["SAM Treatment Rate (%)", "MAM Recovery Rate (%)", "MUAC Screening Coverage (%)"],
    "WASH":          ["Households with Safe Water Access (%)", "Latrines Constructed (#)", "Hygiene Kits Distributed (#)"],
    "Shelter":       ["Families Sheltered (#)", "NFI Kits Distributed (#)", "Transitional Shelters Built (#)"],
    "Protection":    ["GBV Cases Referred (#)", "Child Protection Cases (#)", "Legal Aid Beneficiaries (#)"],
    "Health":        ["Consultations Conducted (#)", "Vaccination Coverage (%)", "Maternal Deaths Avoided (#)"],
    "Food Security": ["Food Rations Distributed (#)", "Cash Transfers Made (#)", "Households Food Secure (%)"],
    "Education":     ["Children Enrolled (#)", "Teachers Trained (#)", "Learning Spaces Rehabilitated (#)"],
}
statuses = ["On Track", "On Track", "On Track", "At Risk", "Delayed"]

# ─── Beneficiaries table ───────────────────────────────────────────
rows_ben = []
ben_id = 1
start = date(2024, 1, 1)
for _ in range(800):
    country = random.choice(countries)
    region  = random.choice(regions[country])
    sector  = random.choice(sectors)
    org_type = random.choice(org_types)
    org = random.choice(orgs[org_type])
    gender = random.choice(["Male","Female","Female"])
    age_group = random.choices(["0-5","6-17","18-59","60+"], weights=[20,30,40,10])[0]
    reg_date = start + timedelta(days=random.randint(0, 450))
    vuln = random.choice(["IDP","Host Community","Refugee","Returnee"])
    rows_ben.append([
        f"BEN-{ben_id:04d}", country, region, sector, org, org_type,
        gender, age_group, vuln, str(reg_date),
        random.choice(donors)
    ])
    ben_id += 1

with open("/home/claude/portfolio/project1_powerbi/data/beneficiaries.csv","w",newline="") as f:
    w = csv.writer(f)
    w.writerow(["BeneficiaryID","Country","Region","Sector","Organization","OrgType",
                "Gender","AgeGroup","VulnerabilityType","RegistrationDate","Donor"])
    w.writerows(rows_ben)

# ─── Activities table ──────────────────────────────────────────────
rows_act = []
act_id = 1
for _ in range(300):
    country = random.choice(countries)
    region  = random.choice(regions[country])
    sector  = random.choice(sectors)
    org_type = random.choice(org_types)
    org = random.choice(orgs[org_type])
    donor = random.choice(donors)
    target = random.randint(100, 5000)
    achieved = int(target * random.uniform(0.40, 1.10))
    budget = round(random.uniform(5000, 200000), 2)
    spent  = round(budget * random.uniform(0.30, 1.05), 2)
    start_d = start + timedelta(days=random.randint(0, 300))
    end_d   = start_d + timedelta(days=random.randint(30, 180))
    status  = random.choice(statuses)
    indic_list = indicators[sector]
    indicator  = random.choice(indic_list)
    rows_act.append([
        f"ACT-{act_id:04d}", country, region, sector, org, org_type, donor,
        indicator, target, achieved, budget, spent,
        str(start_d), str(end_d), status
    ])
    act_id += 1

with open("/home/claude/portfolio/project1_powerbi/data/activities.csv","w",newline="") as f:
    w = csv.writer(f)
    w.writerow(["ActivityID","Country","Region","Sector","Organization","OrgType","Donor",
                "Indicator","Target","Achieved","Budget_USD","Spent_USD",
                "StartDate","EndDate","Status"])
    w.writerows(rows_act)

# ─── Funding table ─────────────────────────────────────────────────
rows_fund = []
fund_id = 1
for _ in range(80):
    country = random.choice(countries)
    sector  = random.choice(sectors)
    donor   = random.choice(donors)
    committed = round(random.uniform(50000, 2000000), 2)
    disbursed = round(committed * random.uniform(0.20, 0.95), 2)
    gap = round(committed * random.uniform(0.05, 0.50), 2)
    yr = random.choice([2023, 2024, 2025])
    rows_fund.append([
        f"FUND-{fund_id:04d}", country, sector, donor,
        committed, disbursed, gap, yr
    ])
    fund_id += 1

with open("/home/claude/portfolio/project1_powerbi/data/funding.csv","w",newline="") as f:
    w = csv.writer(f)
    w.writerow(["FundingID","Country","Sector","Donor","Committed_USD","Disbursed_USD","Gap_USD","Year"])
    w.writerows(rows_fund)

# ─── Incidents / Security table ───────────────────────────────────
rows_inc = []
inc_id = 1
inc_types = ["Armed Conflict","Flood","Drought","Disease Outbreak","Displacement","Food Crisis"]
severity  = ["Low","Medium","High","Critical"]
for _ in range(150):
    country = random.choice(countries)
    region  = random.choice(regions[country])
    inc_type = random.choice(inc_types)
    sev      = random.choice(severity)
    affected = random.randint(500, 50000)
    inc_date = start + timedelta(days=random.randint(0, 450))
    rows_inc.append([
        f"INC-{inc_id:04d}", country, region, inc_type, sev, affected, str(inc_date)
    ])
    inc_id += 1

with open("/home/claude/portfolio/project1_powerbi/data/incidents.csv","w",newline="") as f:
    w = csv.writer(f)
    w.writerow(["IncidentID","Country","Region","IncidentType","Severity","AffectedPopulation","IncidentDate"])
    w.writerows(rows_inc)

# ─── Date table ────────────────────────────────────────────────────
rows_date = []
d = date(2024, 1, 1)
end_d = date(2025, 12, 31)
while d <= end_d:
    rows_date.append([
        str(d), d.year, d.month, d.day,
        d.strftime("%B"), d.strftime("%Y-%m"),
        (d.month - 1) // 3 + 1,
        d.isocalendar()[1],
        d.strftime("%A"),
        1 if d.weekday() >= 5 else 0
    ])
    d += timedelta(days=1)

with open("/home/claude/portfolio/project1_powerbi/data/dim_date.csv","w",newline="") as f:
    w = csv.writer(f)
    w.writerow(["Date","Year","Month","Day","MonthName","YearMonth","Quarter","WeekNumber","DayName","IsWeekend"])
    w.writerows(rows_date)

print("All 5 datasets generated successfully!")
print(f"  beneficiaries.csv : 800 rows")
print(f"  activities.csv    : 300 rows")
print(f"  funding.csv       :  80 rows")
print(f"  incidents.csv     : 150 rows")
print(f"  dim_date.csv      : {len(rows_date)} rows (2024-2025)")
