apt install -y apt-transport-https
apt install -y software-properties-common wget
wget -q -O /usr/share/keyrings/grafana.key https://packages.grafana.com/gpg.key
#echo "deb [signed-by=/usr/share/keyrings/grafana.key] https://packages.grafana.com/enterprise/deb stable main" | sudo tee -a /etc/apt/sources.list.d/grafana.list
echo "deb [signed-by=/usr/share/keyrings/grafana.key] https://packages.grafana.com/enterprise/deb stable main" > /etc/apt/sources.list.d/grafana.list
apt update
apt install -y grafana-enterprise
chown grafana:grafana /var/WEGA/grafana/dashboards -R
cp /var/WEGA/grafana/wega-server.yaml /etc/grafana/provisioning/dashboards/
bash datasource.sh
