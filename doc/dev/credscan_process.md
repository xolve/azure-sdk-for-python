# Guide for monitoring CredScan checks

This guide describes how package owners can monitor their package's Credential Scanner (CredScan) status and correct
any warnings.

General information about CredScan can be found in the overview documentation at [aka.ms/credscan][credscan_doc]. The
Azure SDK's motivation and methodology for running CredScan is documented [here][devops_doc].

## Table of Contents
- [Check CredScan status](#check-credscan-status)
- [Correct active warnings](#correct-active-warnings)
  - [True positives](#true-positives)
  - [False positives](#false-positives)
- [Correct baselined warnings](#correct-baselined-warnings)

## Check CredScan status

CredScan is run each night over the entire `azure-sdk-for-python` repository as part of the
[python - aggregate-reports][aggregate_reports] pipeline. The scan produces a list of active warnings in the "Post
Analysis" task of the "ComplianceTools" job ([example output][credscan_output]).

Each warning will begin with the path to the file containing a potential credential, as well as the row and column where
the credential string begins. For example, for a potential credential that starts in row 3 and column 20 of a
particular file:
```
##[error]sdk/{service}/{package}/{file}.py:sdk/{service}/{package}/{file}.py(3,20)
```

The warning will then list an error code and description of why the potential credential was flagged.

## Correct active warnings

If you find any warnings listed for a package you own, the next step is to determine if the potential credential found
by CredScan is an actual credential (a true positive), or a fake credential/false flag (a false positive).

### True positives

If CredScan discovers an actual credential, please contact the EngSys team at azuresdkengsysteam@microsoft.com so any
remediation can be done.

### False positives

If CredScan flags something that's not actually a credential or secret, we can suppress the warning to shut off the
false alarm. CredScan allows you to suppress fake credentials by either suppressing a string value or by suppressing
warnings for a whole file. **Files that contain more than just fake credentials shouldn't be suppressed.**

Credential warnings are suppressed in [eng/CredScanSuppression.json][suppression_file]. Suppressed string values are in
the `"placeholder"` list, and suppressed files are in the `"file"` list under `"suppressions"`.

If you have a fake credential flagged by CredScan, try one of the following (listed from most to least preferable):
  - Import and use a suitable credential from a file that's already suppressed in [eng/CredScanSuppression.json][suppression_file].
  - Replace the credential with a string value that's already suppressed in [eng/CredScanSuppression.json][suppression_file].
  - Move the credential into a `fake_credentials.py` file in your package, and add the file path to the list of suppressed files if necessary.
  - Add the credential to the list of suppressed string values.

Ideally, fake credential files -- which contain nothing but fake secrets -- should be suppressed and their fake
credentials shouldn't appear in any other files. Sanitizers should be used to keep fake credentials out of test
recordings when possible. String value suppression should be avoided unless the string appears in many files.

Suppressing string values will disable warnings no matter where the string comes up during a scan, but is inefficient
and inconvenient for lengthy strings. Suppressing warnings in a file is convenient for fake credential files, but
strings in that file will still trigger warnings if present in another unsuppressed file.

## Correct baselined warnings

In addition to active warning that appear in the [python - aggregate-reports][aggregate_reports] pipeline ouput, there
are also CredScan warnings that have been suppressed in [eng/python.gdnbaselines][baseline]. This file is a snapshot of
the active warnings at one point in time; CredScan won't re-raise warnings that have been recorded here.

Ultimately, we hope to remove this baseline file from the repository entirely. If you see any warnings for a package
that you own in this file, please remove a few at a time from the file so that CredScan will output these warnings in
the pipeline. Then, resolve them following the steps from the [Correct active warnings](#correct-active-warnings)
section of this guide.


[aggregate_reports]: https://dev.azure.com/azure-sdk/internal/_build?definitionId=1401&_a=summary
[baseline]: https://github.com/Azure/azure-sdk-for-python/blob/main/eng/python.gdnbaselines
[credscan_doc]: https://aka.ms/credscan
[credscan_output]: https://dev.azure.com/azure-sdk/internal/_build/results?buildId=1320151&view=logs&j=3b141548-98d7-5be1-7ef8-eeb08ca02972&t=41e0d8dc-42df-5fff-2417-80cd016cccdb
[devops_doc]: https://dev.azure.com/azure-sdk/internal/_wiki/wikis/internal.wiki/413/Credential-Scan-Step-in-Pipeline
[suppression_file]: https://github.com/Azure/azure-sdk-for-python/blob/main/eng/CredScanSuppression.json
