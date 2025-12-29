# GiveMeLabeledIssues – Text-Based Adaptation

This repository contains an experimental adaptation of the
GiveMeLabeledIssues system. The proposed approach replaces
the dependency on source code analysis with alternative
textual data sources available in OSS repositories, such as
issue titles and descriptions.

## Objective
Adapt the GiveMeLabeledIssues pipeline to recommend OSS
issues using textual information only, and evaluate its
performance against the original approach.

## Implementation
The system implements:
- GitHub issue mining
- Text preprocessing
- TF-IDF representation
- Random Forest classification
- Standard classification metrics

This implementation is designed to run on lightweight
environments (Windows) without requiring CUDA.

## Relation to Original Work
This repository is inspired by:
GiveMeLabeledIssuesAPI (Vargovich et al., MSR 2023)

The original API is not modified. This repository represents
an independent experimental pipeline.
