Verificado el objetivo: crear VM Parrot HTB con KVM/QEMU en Ubuntu. Pasos mínimos, comandos ejecutables, flags y comprobaciones.

# 1. Precondiciones — verificar CPU y preparar sistema

```bash
# verificar extensiones de virtualización
egrep -c '(vmx|svm)' /proc/cpuinfo || { echo "SIN VT-X/AMD-V: no va a acelerar"; exit 1; }

# instalar paquetes (Ubuntu)
sudo apt update


sudo apt install -y qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils virt-manager virt-install

si,falla: 
sudo apt install virt-manager virtinst


# habilitar servicios
sudo systemctl enable --now libvirtd
sudo systemctl status --no-pager libvirtd

# añadir usuario a grupos necesarios (relogin)
sudo usermod -aG libvirt $USER
sudo usermod -aG kvm $USER
```

# 2. Verificaciones rápidas

```bash
# dispositivos kvm
ls -l /dev/kvm

# comprobar que libvirt detecta el hipervisor
virsh -c qemu:///system list --all

# mostrar redes definidas
virsh net-list --all
# la red 'default' suele ser NAT; si no existe:
virsh net-start default
virsh net-autostart default
```

# 3. Preparar almacenamiento (qcow2, snapshots ligeros)

```bash
# crear carpeta si no existe
sudo mkdir -p /var/lib/libvirt/images
sudo chown libvirt-qemu:kvm /var/lib/libvirt/images

# crear disco qcow2 (30 GiB ejemplo)
qemu-img create -f qcow2 /var/lib/libvirt/images/parrot-htb.qcow2 30G

# mostrar info del disco
qemu-img info /var/lib/libvirt/images/parrot-htb.qcow2
```

# 4. Crear la VM desde la ISO (modo texto, reproducible)

Asumiendo: `/home/tuuser/Downloads/Parrot-htb.iso` y recursos: 4 GiB RAM, 4 vCPUs, disco 30G, red NAT `default`.

```bash
sudo virt-install \
  --name parrot-htb \
  --ram 4096 \
  --vcpus 4 \
  --cpu host \
  --disk path=/var/lib/libvirt/images/parrot-htb.qcow2,format=qcow2,bus=virtio \
  --cdrom /home/tuuser/Downloads/Parrot-htb.iso \
  --os-variant debian11 \
  --network network=default,model=virtio \
  --graphics none \
  --console pty,target_type=serial \
  --boot cdrom,hd,menu=on \
  --noautoconsole
```

Explicación de flags críticos:

* `--cpu host` : pasa características reales del CPU (mejor rendimiento).
* `--disk ...,format=qcow2,bus=virtio` : formato y controlador paravirtualizado.
* `--network network=default,model=virtio` : NAT por defecto + virtio.
* `--graphics none` + `--console pty` : instalación por consola (útil en servidores).
* `--noautoconsole` : evita atarlo al tty actual; conecta con `virsh` o `virt-manager`.

Conectar a la consola de instalación:

```bash
# ver lista de dominios para obtener id o nombre
virsh list --all
# conectar
virsh console parrot-htb
# salir: Ctrl-]  (o Ctrl+] dependiendo)
```

Si preferís GUI:

```bash
virt-manager
# abrir la VM parrot-htb, doble click y seguir instalación gráfica.
```

# 5. Optimización post-instalación

```bash
# instalar drivers paravirtuales dentro del guest (si no vienen)
# en Debian/Parrot guest:
sudo apt update
sudo apt install -y linux-headers-$(uname -r) qemu-guest-agent spice-vdagent

# activar qemu-guest-agent (desde guest)
sudo systemctl enable --now qemu-guest-agent

# en host: habilitar canales para shutdown/graceful
virsh shutdown parrot-htb
virsh start parrot-htb

# snapshot ejemplo (antes de pruebas)
virsh snapshot-create-as --domain parrot-htb pre-tryhackme "Snapshot inicial" --disk-only --atomic
```

# 6. Passthrough (si necesitas USB o GPU; resumen directo)

* USB: `virsh attach-device` con XML que mapea vendor\:product.
* GPU passthrough: requiere IOMMU habilitado en kernel (`intel_iommu=on` o `amd_iommu=on`) en grub, aislamiento de dispositivos con vfio, y mapeo PCI en xml. Es complejo; pide si querés el flujo completo.

# 7. Resumen de flujo de creación

1. Verificar VT-x/AMD-V.
2. Instalar paquetes y habilitar libvirt.
3. Crear disco qcow2.
4. `virt-install` con `--cdrom` o usar `virt-manager`.
5. Instalar `qemu-guest-agent` dentro del guest.
6. Snapshotar antes de pruebas agresivas.

Si querés —sin preguntar— procedo a:

* generar el archivo XML de libvirt para passthrough USB específico y ejemplo de `virsh attach-device`;
* o te doy el comando `virt-install` adaptado a recursos distintos (RAM/VCPU/disk) que indiques.
