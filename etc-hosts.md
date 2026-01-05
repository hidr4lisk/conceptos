# /etc/hosts

´´´
echo "10.64.157.30 lists.tryhackme.loc" | sudo tee -a /etc/hosts

´´´

Si no usás -a, pisás el archivo completo.


echo "10.66.188.21 httprequestsmuggling.thm" | sudo tee -a /etc/hosts