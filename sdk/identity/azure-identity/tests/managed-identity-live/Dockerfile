# ------------------------------------
# Copyright (c) Microsoft Corporation.
# Licensed under the MIT License.
# ------------------------------------
ARG PYTHON_VERSION=3.9

# docker can't tell when the repo has changed and will therefore cache this layer
FROM alpine/git as repo
RUN git clone https://github.com/Azure/azure-sdk-for-python --single-branch --depth 1 /azure-sdk-for-python


FROM python:${PYTHON_VERSION}-slim

COPY --from=repo /azure-sdk-for-python/sdk/identity /sdk/identity
COPY --from=repo /azure-sdk-for-python/sdk/core/azure-core /sdk/core/azure-core
COPY --from=repo /azure-sdk-for-python/sdk/keyvault/azure-keyvault-secrets /sdk/keyvault/azure-keyvault-secrets

WORKDIR /sdk/identity/azure-identity/tests/managed-identity-live
RUN pip install --no-cache-dir -r requirements.txt

CMD [ "pytest", "-rs", "-v", "--log-level=DEBUG" ]
