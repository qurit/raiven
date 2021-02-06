Conf

## API Settings

## Authentication

### LDAP
| Env Var | Description | Default |
| --- | --- | --- |
| LDAP_ENABLED | Should RAIVEN use LDAP as a means of authentication | False
| LDAP_HOST | IP address of the LDAP server |  |
| LDAP_PORT | Port of the LDAP server | 389
| LDAP_USE_SSL | SSL Enabled | False
| LDAP_USERNAME_BASE | User name base |
| LDAP_BASE_DN | Base DN |
| LDAP_SEARCH_FILTER | LDAP search filter | (&(objectCategory=person)(objectClass=user)(sAMAccountName=%s))

## DICOM
| Env Var | Description | Default |
| --- | --- | --- |
| SCP_AE_TITLE | AE Title of RAIVEN's built in DICOM server | `RAIVEN`
| SCP_PORT | Port of RAIVEN's built in DICOM server  | `11112`
| SCP_HOST | Host of RAIVEN's built in DICOM server. If running in docker this should be set to `0.0.0.0`  | `127.0.0.1`
| SCP_DEBUG | Display DICOM server debug information | `False`