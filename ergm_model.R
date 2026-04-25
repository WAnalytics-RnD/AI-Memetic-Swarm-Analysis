library(tidyverse)
library(ergm)
library(network)

edges <- read_csv("mutation_edges.csv")
nodes <- read_csv("tweets_final.csv")

# Map tweet IDs to integer indices
id_map <- setNames(seq_len(nrow(nodes)), as.character(nodes$id))

edge_source <- id_map[as.character(edges$source)]
edge_target <- id_map[as.character(edges$target)]

# Filter to valid edges
valid <- !is.na(edge_source) & !is.na(edge_target)
edge_mat <- matrix(c(edge_source[valid], edge_target[valid]), ncol = 2)

# Sample 500 nodes for tractable ERGM estimation
set.seed(42)
sample_ids <- sample(seq_len(nrow(nodes)), 500)
nodes_s <- nodes[sample_ids, ]

edge_source_s <- id_map[as.character(edges$source)]
edge_target_s <- id_map[as.character(edges$target)]

valid_s <- edge_source_s %in% sample_ids & edge_target_s %in% sample_ids
edge_source_s <- match(edge_source_s[valid_s], sample_ids)
edge_target_s <- match(edge_target_s[valid_s], sample_ids)

edge_mat_s <- matrix(c(edge_source_s, edge_target_s), ncol = 2)

# Build network object
net_s <- network(edge_mat_s, directed = TRUE, vertices = 500)
net_s %v% "ai_generated" <- nodes_s$ai_generated
net_s %v% "virality_score" <- nodes_s$virality_score

# Fit ERGM
model <- ergm(
  net_s ~ edges + nodematch("ai_generated") + nodecov("virality_score"),
  control = control.ergm(MCMC.samplesize = 2000, MCMC.burnin = 5000)
)

summary(model)
