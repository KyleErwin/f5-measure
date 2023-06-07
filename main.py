import pandas as pd


def update_if_longer(dict, key, xs):
    if key in dict:
        dict[key] = dict[key] if len(dict[key]) > len(xs) else xs
    else:
        dict[key] = xs


def longest_sequences(df, feature, target_feature="target"):
    df = df.sort_values(feature)[[feature, target_feature]]

    longest = {}
    sequences = []

    prev_target = None
    indices = []

    for j, (idx, _, target) in enumerate(df.itertuples(name=None)):
        if target != prev_target and j > 0:
            sequences.append((prev_target, indices))
            update_if_longer(longest, prev_target, indices)
            indices = []

        prev_target = target
        indices.append(idx)

        if j == len(df) - 1:
            sequences.append((target, indices))
            update_if_longer(longest, prev_target, indices)

    head_target, head_indices = sequences[0]
    tail_target, tail_indices = sequences[-1]

    if head_target == tail_target:
        indices = head_indices + tail_indices
        # sequences.append((head_target, indices))
        update_if_longer(longest, head_target, indices)

    return longest


def f5_complexity(df, target_feature="target"):
    start_df_len = len(df)
    features = df.columns.drop(target_feature).tolist()

    while len(features) and len(df):
        # md is shorthand here for most discriminative
        md_feature = None
        md_indices = []

        for feature in features:
            sequences = longest_sequences(df, feature, target_feature)
            indices = []

            for _, xs in sequences.items():
                indices = indices + xs

            if  len(indices) > len(md_indices):
                md_feature = feature
                md_indices = indices
        features.remove(md_feature)
        df = df.drop(md_indices)

    return len(df) / start_df_len


def main():
    datasets = [
        "clusters",
        "clusters-overlap",
        "oblique",
        "3-columns",
        "5-columns",
        "moons",
        "circles",
        "random-imbalanced",
        "random",
    ]

    path = "two-class"

    for dataset in datasets:
        df = pd.read_csv(f"datasets/{path}/{dataset}.csv")
        f5 = f5_complexity(df)
        print(f"{path}/{dataset}: {f5}")


if __name__ == '__main__':
    main()
