import random
import math

class Individual:
    def __init__(self, genes):
        self.genes = genes
        self.fitness = 0.0


def calculate_feature_scores(df):
    N_FEATURES = df.shape[1]
    X = df.values.tolist()
    y = [sum(row[:5]) + random.random() * 0.5 for row in X]

    scores = [0.0] * N_FEATURES
    mean_Y = sum(y) / len(y)

    for i in range(N_FEATURES):
        feature_col = [row[i] for row in X]
        mean_X = sum(feature_col) / len(feature_col)
        cov = sum((feature_col[j]-mean_X)*(y[j]-mean_Y) for j in range(len(X)))
        std_X_sq = sum((feature_col[j]-mean_X)**2 for j in range(len(X)))
        std_Y_sq = sum((y[j]-mean_Y)**2 for j in range(len(X)))
        denominator = math.sqrt(std_X_sq * std_Y_sq)
        scores[i] = abs(cov/denominator) if denominator != 0 else 0.0

    return scores


def evaluate(individual, feature_scores, num_features):
    selected = [i for i, g in enumerate(individual.genes) if g == 1]
    if not selected:
        return 0
    stat_score = sum(feature_scores[i] for i in selected)
    return stat_score - 0.5 * len(selected) / num_features


def init_population(pop_size, num_features):
    return [Individual([random.randint(0, 1) for _ in range(num_features)]) for _ in range(pop_size)]


def clone_individual(ind):
    new_ind = Individual(list(ind.genes))
    new_ind.fitness = ind.fitness
    return new_ind


def crossover(parent1, parent2):
    size = len(parent1.genes)
    pt = random.randint(1, size - 1)
    child1 = Individual(parent1.genes[:pt] + parent2.genes[pt:])
    child2 = Individual(parent2.genes[:pt] + parent1.genes[pt:])
    return child1, child2


def mutate(ind, indpb):
    for i in range(len(ind.genes)):
        if random.random() < indpb:
            ind.genes[i] = 1 - ind.genes[i]


def tournament_selection(population, k):
    aspirants = random.choices(population, k=k)
    return max(aspirants, key=lambda ind: ind.fitness)


def run_ga_on_df(df):
    N_FEATURES = df.shape[1]
    feature_scores = calculate_feature_scores(df)

    POP_SIZE, NGEN = 50, 30
    CXPB, MUTPB, TOURN = 0.5, 0.2, 3
    INDPB = 1.0 / N_FEATURES

    population = init_population(POP_SIZE, N_FEATURES)
    for ind in population:
        ind.fitness = evaluate(ind, feature_scores, N_FEATURES)

    best = None
    generations_stats = []

    for gen in range(NGEN):
        offspring = [clone_individual(tournament_selection(population, TOURN)) for _ in range(POP_SIZE)]

        for i in range(0, POP_SIZE, 2):
            if i + 1 < POP_SIZE and random.random() < CXPB:
                child1, child2 = crossover(offspring[i], offspring[i + 1])
                offspring[i], offspring[i + 1] = child1, child2

            mutate(offspring[i], INDPB)
            if i + 1 < POP_SIZE:
                mutate(offspring[i + 1], INDPB)

        for ind in offspring:
            ind.fitness = evaluate(ind, feature_scores, N_FEATURES)

        population = offspring
        current_best = max(population, key=lambda ind: ind.fitness)

        if best is None or current_best.fitness > best.fitness:
            best = clone_individual(current_best)

        fits = [ind.fitness for ind in population]
        avg_fit = sum(fits) / len(fits)
        max_fit = max(fits)

        generations_stats.append({
            "generation": gen,
            "best_genes": current_best.genes,
            "best_fitness": max_fit,
            "avg_fitness": avg_fit
        })

    selected_indices = [i for i, g in enumerate(best.genes) if g == 1]

    return {
        "best_chromosome": best.genes,
        "selected_features": selected_indices,
        "fitness": best.fitness,
        "generations_stats": generations_stats
    }
