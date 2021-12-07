sudo apt-get update
sudo apt-get upgrade
sudo apt-get install libatlas-base-dev
sudo apt install python3-venv
sleep(1)
mkdir /opt/test
cd /opt/test
sudo python3 -m venv env
python3 -m venv my-project-env
sleep(1)
source env/bin/activate



sudo pip3 install pyaudio
sudo pip3 install scipy
sudo pip3 install pixel-ring
sudo pip3 install gpiozero