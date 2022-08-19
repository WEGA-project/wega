import bjoern
import argparse
parser = argparse.ArgumentParser(description='bjorn port')
parser.add_argument('--port', type=int, default=5003, help='provide an integer (default: 5003)')
args = parser.parse_args()
print(args.port)
from project.wsgi import application as  wsgi_application
port = args.port
bjoern.run(wsgi_application, '0.0.0.0', port)


