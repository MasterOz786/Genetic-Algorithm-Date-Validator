import random
from typing import List, Tuple, Dict, Set
from dataclasses import dataclass
from datetime import datetime
Tareekh = Tuple[int, int, int]
Jamaa = List[Tareekh]

@dataclass
class Misaal:
    tareekh: Tareekh
    qism: str
    sahi_ha: bool

def leap_ka_jach(saal: int) -> bool:
  return saal % 4 == 0 and (saal % 100 != 0 or saal % 400 == 0)

def date_theek_ha(tareekh: Tareekh) -> bool:
  din, mahina, saal = tareekh
  if not (0 <= saal <= 9999):
    return False
  if not (1 <= mahina <= 12):
    return False
  if not (1 <= din <= 31):
    return False
  mahine_ke_din = [0,31,28,31,30,31,30,31,31,30,31,30,31]
  if leap_ka_jach(saal):
    mahine_ke_din[2] = 29
  return din <= mahine_ke_din[mahina]

def tareekh_ki_qism(tareekh: Tareekh) -> str:
  din, mahina, saal = tareekh
  if not (0 <= saal <= 9999):
    return "Ghalat_Saal"
  if not (1 <= mahina <= 12):
    return "Ghalat_Mahina"
  if not (1 <= din <= 31):
    return "Ghalat_Din"
  if mahina == 2:
    if leap_ka_jach(saal):
      if din == 29:
        return "Sahi_Leap_Feb29"
      elif din > 29:
        return "Ghalat_Leap_Feb"
    else:
      if din > 28:
        return "Ghalat_NonLeap_Feb"
  din_per_mahina = [0,31,28,31,30,31,30,31,31,30,31,30,31]
  if din > din_per_mahina[mahina]:
    return f"Ghalat_Din_Mahina_{mahina}"
  if din == 31 and mahina in [1,3,5,7,8,10,12]:
    return "Sahi_31_Din"
  if din == 30 and mahina in [4,6,9,11]:
    return "Sahi_30_Din"
  if saal in [0,9999]:
    return "Had_Basta_Saal"
  return "Sahi_Saada_Tareekh"

def random_tareekh_banao() -> Tareekh:
  return (random.randint(0,32), random.randint(0,13), random.randint(-1,10000))

def shuru_jamaa(size: int) -> Jamaa:
  return [random_tareekh_banao() for _ in range(size)]

def fitness_nikaal(tareekhein: Jamaa) -> float:
  qism_set: Set[str] = set()
  qism_count: Dict[str,int] = {}
  for t in tareekhein:
    q = tareekh_ki_qism(t)
    qism_set.add(q)
    qism_count[q] = qism_count.get(q,0) + 1
  score = len(qism_set)
  penalty = sum(count - 1 for count in qism_count.values())
  return score - (0.5 * penalty)

def jod_shod(bhai1: Tareekh, bhai2: Tareekh) -> Tareekh:
  choice = [random.random() < 0.5 for _ in range(3)]
  return (bhai1[0] if choice[0] else bhai2[0],
          bhai1[1] if choice[1] else bhai2[1],
          bhai1[2] if choice[2] else bhai2[2])

def badal_de(tareekh: Tareekh, mutation_rate: float) -> Tareekh:
  din, mahina, saal = tareekh
  if random.random() < mutation_rate:
    din += random.randint(-3,3)
  if random.random() < mutation_rate:
    mahina += random.randint(-1,1)
  if random.random() < mutation_rate:
    saal += random.randint(-100,100)
  return (din, mahina, saal)

def chun_lo_bhai(jamaa: Jamaa, num: int) -> Jamaa:
  ret = []
  for _ in range(num):
    tour = random.sample(jamaa, k=3)
    tour.sort(key=lambda x: fitness_nikaal([x]), reverse=True)
    ret.append(tour[0])
  return ret

def badalte_raho(jamaa: Jamaa, mutation_rate: float = 0.15, elite_size: int = 2) -> Jamaa:
  n = len(jamaa)
  jamaa.sort(key=lambda x: fitness_nikaal([x]), reverse=True)
  new_jamaa = jamaa[:elite_size]
  while len(new_jamaa) < n:
    parents = chun_lo_bhai(jamaa, 2)
    child = jod_shod(parents[0], parents[1])
    child = badal_de(child, mutation_rate)
    new_jamaa.append(child)
  return new_jamaa

def chala_daal_algorithm(pop_size: int = 50, generations: int = 100, mutation_rate: float = 0.15, target_coverage: float = 0.95) -> Tuple[Jamaa, List[float]]:
  jamaa = shuru_jamaa(pop_size)
  history = []
  for gen in range(generations):
    jamaa = badalte_raho(jamaa, mutation_rate)
    best = fitness_nikaal(jamaa)
    history.append(best)
    print(f"Gen {gen}: Best Score = {best:.2f}")
    if best >= target_coverage * 13:
      print(f"Bhai, target cover ho gaya at Gen {gen}")
      break
  return jamaa, history

def tareekh_format(tareekh: Tareekh) -> str:
  return f"{tareekh[0]:02d}/{tareekh[1]:02d}/{tareekh[2]:04d}"

def natija_dekho(jamaa: Jamaa) -> None:
  qisms: Dict[str, List[Tareekh]] = {}
  for t in jamaa:
    q = tareekh_ki_qism(t)
    if q not in qisms:
      qisms[q] = []
    qisms[q].append(t)
  print("\nTest Cases ki Jaanch:")
  print("=" * 50)
  for q, ts in qisms.items():
    print(f"\n{q}:")
    for t in ts[:3]:
      print(f"  {tareekh_format(t)}")
  cov = len(qisms) / 13 * 100
  print(f"\nQism Coverage: {cov:.2f}%")

def chlo_gee():
  print("Chalo bhai, GA shuru kar rahe hain...")
  jamaa, hist = chala_daal_algorithm()
  print("\nGA complete ho gaya!")
  natija_dekho(jamaa)
  with open("test_cases.txt", "w") as f:
    f.write("Banae hue test cases:\n")
    f.write("=" * 50 + "\n")
    for t in jamaa:
      q = tareekh_ki_qism(t)
      f.write(f"{tareekh_format(t)} - {q}\n")

chlo_gee()