# Amaranta Record

Code and configs related to our record player setup at Amaranta.

## Requirements

- Python 3.7 (pip and virtualenv)
- ices2
- icecast

## Production
To check what's going on (look at the logs) run these:

```
# ices2
cat /var/log/ices/ices.log
# icecast
sudo journalctl -u icecast -f
# amaranta_record script
sudo journalctl -u amaranta_record -f
```
