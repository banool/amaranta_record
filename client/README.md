# Client

This describes how to subscribe to the stream that we set up following the guide in the root directory. This doesn't use the Chromecast approach at all, it just takes the icebox stream from the source raspberry pi, listens to it, and then outputs it through the audio jack of the receiver raspberry pi. This works if the receiver pi is connected to another audio system for example.

Essentially all we're doing here is checking if the stream is up periodically and if so, playing it.

If you're running this on the same machine as the server (e.g. to then play via Bluetooth), you can change the URL in the config file to 127.0.0.1.

Add playstream.service to /etc/systemd/system/playstream.service

Then run this:
```
sudo systemctl enable playstream.service
sudo systemctl start playstream.service
```
