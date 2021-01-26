## Where to put the configs
ices.xml -> /etc/ices.xml
icecast.xml -> /etc/icecast2/icecast.xml
amaranta_record.service -> /etc/systemd/system/amaranta_record.service
icecast.service -> /etc/systemd/system/icecast.service

## Registering it all

Do this once you've copied all the config files in.

```
sudo systemctl daemon-reload
```
```
sudo systemctl enable amaranta_record
sudo systemctl start amaranta_record
```
```
sudo systemctl enable icecast
sudo systemctl start icecast
```
