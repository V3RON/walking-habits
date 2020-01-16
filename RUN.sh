
pip3 install -r requirements.txt
pip3 install -e .
bash -c 'sleep 10; open http://localhost:8050' &
run-walking_habits-dev
