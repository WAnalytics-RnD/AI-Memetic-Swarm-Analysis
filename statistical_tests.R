library(tidyverse)
library(rstatix)

df <- read_csv("tweets_final.csv")

# Load composite classified data
df_v3 <- read_csv("tweets_v3.csv")
final <- read_csv("tweets_final.csv")

df_v3 <- df_v3 %>% left_join(final %>% select(id, virality_score, degree, clustering), by = "id")

# Filter to high-confidence AI and human only
df_binary <- df_v3 %>%
  filter(composite_ai != 1) %>%
  mutate(ai_group = ifelse(composite_ai == 2, 1, 0))

ai <- df_binary %>% filter(ai_group == 1) %>% pull(virality_score)
human <- df_binary %>% filter(ai_group == 0) %>% pull(virality_score)

# Descriptive statistics
df_binary %>%
  group_by(ai_group) %>%
  summarise(
    n = n(),
    mean_virality = mean(virality_score, na.rm = TRUE),
    median_virality = median(virality_score, na.rm = TRUE)
  )

# Wilcoxon rank-sum test
wilcox.test(ai, human, alternative = "greater")

# Welch t-test
t.test(ai, human, alternative = "greater")

# Effect size
df_binary %>%
  mutate(ai_group = as.factor(ai_group)) %>%
  wilcox_effsize(virality_score ~ ai_group)

# Cohen's d
pooled_sd <- sqrt((sd(ai, na.rm = TRUE)^2 + sd(human, na.rm = TRUE)^2) / 2)
cat("Cohen's d:", round((mean(ai, na.rm = TRUE) - mean(human, na.rm = TRUE)) / pooled_sd, 4), "\n")

# Permutation test
set.seed(42)
ai_clean <- ai[!is.na(ai)]
human_clean <- human[!is.na(human)]
observed_diff <- mean(ai_clean) - mean(human_clean)
all_scores <- c(ai_clean, human_clean)
n_ai <- length(ai_clean)

perm_diffs <- replicate(1000, {
  shuffled <- sample(all_scores)
  mean(shuffled[1:n_ai]) - mean(shuffled[(n_ai + 1):length(shuffled)])
})

cat("Observed difference:", round(observed_diff, 4), "\n")
cat("Permutation p-value:", round(mean(perm_diffs >= observed_diff), 4), "\n")
