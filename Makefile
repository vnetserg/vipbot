
# Be default, do nothing

all:


# Cleaning targets:

clean: clean-setup clean-build clean-pyc

clean-setup:
	python setup.py clean --all

clean-build:
	rm -rfv build/
	rm -rfv dist/
	rm -rfv .eggs/
	find . -name '*.egg-info' -exec rm -rfv {} +
	find . -name '*.egg' -exec rm -rfv {} +

clean-pyc:
	find . -name '*.pyc' -exec rm -rfv {} +
	find . -name '*.pyo' -exec rm -rfv {} +
	find . -name '*~' -exec rm -rfv {} +
	find . -name '__pycache__' -exec rm -rfv {} +


# Installation target

install:
	bash ./setupvenv.sh
	cp vipbot.yaml /etc/vipbot.yaml
	cp vipbot.sh /usr/bin/vipbot
	cp vipbot.service /lib/systemd/system/vipbot.service


# Uninstallation target

uninstall:
	rm -rf /opt/vipbot
	rm -rf /usr/bin/vipbot