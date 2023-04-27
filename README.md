# Muted Issues

This utility will automatically close **fully muted** issues that are still open after a muting window's period ends, allowing for notifications to re-trigger for those previously muted issues.

**NOTE**

Host not reporting or signal loss triggered conditions will not be auto-closed. If no data is still not reporting back to New Relic post muting window, then closing that issue will not automatically re-trigger an issue. These cases are handled by writing a separate event back to New Relic, on each execution of this utility, under the **`SignalLossPersistAfterMutingWindow`** eventType. This can be used to generate NRQL alerts and will represent data is _still_ not reporting for any entities, after a muting period ends.

## Requirements
 - Python3+
 - requests module - `pip install requests`
 - New Relic user key, license key, and accountId

## Testing
  0. Validate requirements above
  1. Input user/license keys and accountId into main.py `config` section
  2. Run `python[3] main.py`

## Running
It is recommended to run `main.py` on a set, automated schedule - typically every 10-60 minutes. Below are helpful links to get you started, depending on your OS.

 - [Cronjobs in Linux](https://www.cyberciti.biz/faq/how-do-i-add-jobs-to-cron-under-linux-or-unix-oses/)
 - [Task scheduler in Windows](https://www.jcchouinard.com/python-automation-using-task-scheduler/)

## Troubleshooting
 - Each execution's results are written back to NRDB, to a custom eventType **`CloseMutedIssueResult`** - This can be used to configure alerts or dashboards to keep track of the utility's status/results.
 - Logs are written to a `muting.log` file in the same directory as `main.py`
 - Debug logging can be enabled within `main.py` - change the `level` to `logging.DEBUG`
