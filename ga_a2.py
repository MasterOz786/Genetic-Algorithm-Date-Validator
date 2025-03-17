import random
from typing import List, Tuple, Dict
from dataclasses import dataclass

# Define types and constants
Tareekh = Tuple[int, int, int]
Jamaa = List[Tareekh]
TOTAL_QISMS = 13

@dataclass
class Misaal:
    tareekh: Tareekh
    qism: str
    sahi_ha: bool

def leap_ka_jach(saal: int) -> bool:
    return saal % 4 == 0 and (saal % 100 != 0 or saal % 400 == 0)

def date_theek_ha(t: Tareekh) -> bool:
    din, mahina, saal = t
    if not (0 <= saal <= 9999):
        return False
    if not (1 <= mahina <= 12):
        return False
    if not (1 <= din <= 31):
        return False
    mahine_ke_din = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if leap_ka_jach(saal):
        mahine_ke_din[2] = 29
    return din <= mahine_ke_din[mahina]

def tareekh_ki_qism(t: Tareekh) -> str:
    din, mahina, saal = t
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
    din_per_mahina = [0, 31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    if din > din_per_mahina[mahina]:
        return f"Ghalat_Din_Mahina_{mahina}"
    if din == 31 and mahina in [1, 3, 5, 7, 8, 10, 12]:
        return "Sahi_31_Din"
    if din == 30 and mahina in [4, 6, 9, 11]:
        return "Sahi_30_Din"
    if saal in [0, 9999]:
        return "Had_Basta_Saal"
    return "Sahi_Saada_Tareekh"

def random_tareekh_banao() -> Tareekh:
    return (random.randint(0, 32), random.randint(0, 13), random.randint(-1, 10000))

def shuru_jamaa(size: int) -> Jamaa:
    return [random_tareekh_banao() for _ in range(size)]

def compute_frequencies(jamaa: Jamaa) -> Dict[str, int]:
    freq = {}
    for t in jamaa:
        cat = tareekh_ki_qism(t)
        freq[cat] = freq.get(cat, 0) + 1
    return freq

# Individual fitness based on rarity: rarer categories get a higher score.
def individual_fitness(t: Tareekh, freq: Dict[str, int]) -> float:
    return 1.0 / freq[tareekh_ki_qism(t)]

# Tournament selection using individual fitness based on rarity
def chun_lo_bhai(jamaa: Jamaa, num: int) -> Jamaa:
    ret = []
    freq = compute_frequencies(jamaa)
    for _ in range(num):
        tour = random.sample(jamaa, k=3)
        tour.sort(key=lambda x: individual_fitness(x, freq), reverse=True)
        ret.append(tour[0])
    return ret

def jod_shod(bhai1: Tareekh, bhai2: Tareekh) -> Tareekh:
    choice = [random.random() < 0.5 for _ in range(3)]
    return (bhai1[0] if choice[0] else bhai2[0],
            bhai1[1] if choice[1] else bhai2[1],
            bhai1[2] if choice[2] else bhai2[2])

def badal_de(t: Tareekh, mutation_rate: float) -> Tareekh:
    din, mahina, saal = t
    if random.random() < mutation_rate:
        din += random.randint(-3, 3)
    if random.random() < mutation_rate:
        mahina += random.randint(-1, 1)
    if random.random() < mutation_rate:
        saal += random.randint(-100, 100)
    return (din, mahina, saal)

def badalte_raho(jamaa: Jamaa, mutation_rate: float = 0.4, elite_size: int = 2) -> Jamaa:
    n = len(jamaa)
    # Elite preservation: keep best individuals (here best = having rare categories)
    jamaa.sort(key=lambda x: tareekh_ki_qism(x))
    new_jamaa = jamaa[:elite_size]
    while len(new_jamaa) < n:
        parents = chun_lo_bhai(jamaa, 2)
        child = jod_shod(parents[0], parents[1])
        child = badal_de(child, mutation_rate)
        new_jamaa.append(child)
    return new_jamaa

# Overall fitness: number of unique qisms in the population.
def overall_fitness(jamaa: Jamaa) -> int:
    unique = len({tareekh_ki_qism(t) for t in jamaa})
    return unique

def chala_daal_algorithm(pop_size: int = 300, generations: int = 300, mutation_rate: float = 0.4, target_coverage: float = 0.90) -> Tuple[Jamaa, List[int]]:
    jamaa = shuru_jamaa(pop_size)
    history = []
    print("GA starting with population size:", pop_size)
    for gen in range(generations):
        jamaa = badalte_raho(jamaa, mutation_rate)
        unique = overall_fitness(jamaa)
        history.append(unique)
        freq = compute_frequencies(jamaa)
        # Detailed log per generation
        print(f"Gen {gen}: Unique Qisms = {unique} out of {TOTAL_QISMS} | Frequencies: {freq}")
        # Target: 90% coverage (i.e. at least 12 unique categories)
        if unique >= target_coverage * TOTAL_QISMS:
            print(f"Bhai, target coverage reached at Gen {gen}")
            break
    return jamaa, history

def tareekh_format(t: Tareekh) -> str:
    return f"{t[0]:02d}/{t[1]:02d}/{t[2]:04d}"

def final_test_cases(jamaa: Jamaa) -> Tuple[List[Tareekh], List[Tareekh]]:
    valid = [t for t in jamaa if date_theek_ha(t)]
    invalid = [t for t in jamaa if not date_theek_ha(t)]
    while len(valid) < 10:
        cand = random_tareekh_banao()
        if date_theek_ha(cand):
            valid.append(cand)
    while len(invalid) < 10:
        cand = random_tareekh_banao()
        if not date_theek_ha(cand):
            invalid.append(cand)
    return valid[:10], invalid[:10]

def calculate_coverage(valid: List[Tareekh], invalid: List[Tareekh]) -> float:
    sab = valid + invalid
    unique = len({tareekh_ki_qism(t) for t in sab})
    return (unique / TOTAL_QISMS) * 100

def natija_dekho(jamaa: Jamaa) -> None:
    valid = [t for t in jamaa if date_theek_ha(t)]
    invalid = [t for t in jamaa if not date_theek_ha(t)]
    print("\nSahi Tareekh (Valid):")
    print("=" * 30)
    for t in valid[:10]:
        print(f"  {tareekh_format(t)}")
    print("\nGhalat Tareekh (Invalid):")
    print("=" * 30)
    for t in invalid[:10]:
        print(f"  {tareekh_format(t)}")
    cov = calculate_coverage(valid[:10], invalid[:10])
    print(f"\nQism Coverage: {cov:.2f}%")

def main():
    print("Chalo bhai, GA shuru kar rahe hain...")
    jamaa, hist = chala_daal_algorithm()
    print("\nGA complete ho gaya!")
    valid, invalid = final_test_cases(jamaa)
    print("\nFinal Test Cases (10 Valid & 10 Invalid):")
    print("=" * 50)
    print("\nValid Dates:")
    for t in valid:
        print(f"  {tareekh_format(t)}")
    print("\nInvalid Dates:")
    for t in invalid:
        print(f"  {tareekh_format(t)}")
    cov = calculate_coverage(valid, invalid)
    print(f"\nOverall Qism Coverage: {cov:.2f}%")
    with open("test_cases.txt", "w") as f:
        f.write("Final Test Cases (10 Valid & 10 Invalid):\n")
        f.write("=" * 50 + "\n")
        f.write("\nValid Dates:\n")
        for t in valid:
            f.write(f"{tareekh_format(t)}\n")
        f.write("\nInvalid Dates:\n")
        for t in invalid:
            f.write(f"{tareekh_format(t)}\n")
        f.write(f"\nOverall Qism Coverage: {cov:.2f}%\n")

if __name__ == "__main__":
    main()
