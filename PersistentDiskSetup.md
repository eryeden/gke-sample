# Persistent disk setup


## コンテンツ
1. Persistent volumeにデータをGCSからダウンロードして、ダウンロード用のPodを消す。
2. データをすでにダウンロードしてあるPersistent volumeを別Podからマウントする。
3. 別Pod内に入りPersistent volumeにデータが入っているか確認する。

基本的にやること: https://cloud.google.com/kubernetes-engine/docs/how-to/persistent-volumes/readonlymany-disks


## 事前準備
Localでgcloudを使えるように事前設定する。kubectlコマンドも利用できるように設定する。
``` bash
# setting gcloud
gcloud init

# Update components
gcloud components update
gcloud components update kubectl
```

## 事前準備
なにかしらのクラスタをGKE上に作成する必要がある。
デフォルトでGKEクラスタを作成すると、`n1-standard`クラスのマシンがGCE上に確保される。ここで性能はほとんど必要無いのでもっと安いマシンで良い気がする。
そこで、ここでは`e2-small`を１つのみ含むクラスタを作成することにする。`f1-micro`,`g1-small`くらいだとメモリ不足でGKEが安定していないらしいのでメモリ2G使える`e2-small`にする。


```bash
#Set CLUSTER_NAM and NODE_POOL
CLUSTER_NAME="gke-test-cluster"
ZONE="us-central1-c"

# Create cluster and nodes
gcloud container clusters create $CLUSTER_NAME --machine-type=e2-small --num-nodes 1 --disk-size 10 --zone $ZONE
# Fetch the credential
gcloud container clusters get-credentials $CLUSTER_NAME --zone=$ZONE
```

参考: https://sleepless-se.net/2018/12/11/gke-kubernetes/

### Tips
GKEの自動アップデートの自動アップデートがかかるとkubectlなど制御ができなくなる。クラスター作成時に`--no-enable-autoupgrade`をつける。


## 1. Persistent volumeの自動準備
`PersistentVolumeClaims`をk8sで作成することで、Persistent volumeを自動的に作成することができる。

- `PersistentVolumeClaims`
Persistent volumeを生成するリクエストのようなもの。このリクエストは設定ファイルとしてYAMLを書き、これをk8sにapplyするこで設定される。

- `PersistentVolume`
実際のVolumeの定義に相当する。`PersistentVolumeClaims`から自動的に、明示的にユーザーが`PersistentVolume`を定義しなくても、作成することができる。
GKEの場合、`PersistentVolumeClaims`で自動的に`PersistentVolume`を生成できる（自動プロビジョニング）できるため、直接設定・作成しなくてよい。

- `StorageClass`
生成されるStorageの設定が可能。ここで、高速なSSDをつかう設定も可能。重要な`reclaimPolicy`の設定も可能。
ここで設定した`StorageClass`をClaim時に設定することができる。

### Persistent volumeの自動生成方法
生成するVolumeの設定：

| Option             | Value         | Configuration category | Description                                                                                                          |
| ------------------ | ------------- | ---------------------- | -------------------------------------------------------------------------------------------------------------------- |
| Reclaim policy     | Retain        | StorageClass           | StorageClassで設定する。`Retain`にすることで、Claimが削除されたあともVolumeは削除されず残る。                        |
| Storage type       | pd-standard   | StorageClass           | StorageClassで設定。性能など選べる。[ディクスタイプ参照](https://cloud.google.com/compute/docs/disks#disk-types)。   |
| Storage class name | pd-example    | StorageClass           | PersistentVolumeClaimsでStorageClassの指定に利用する名前                                                             |
| Claim name         | pvc-demo      | PersistentVolumeClaim  | Podの設定などから作成したVolumeClaimを参照するときに使う名前                                                         |
| Access modes       | ReadWriteOnce | PersistentVolumeClaim  | 参照するPodのアクセス権限。ReadWriteOnceだと一つのPodが読み書きできる。複数Podから同時にマウントすることはできない。 |
| Storage size       | 30Gi          | PersistentVolumeClaim  | 確保するVolumeのサイズ                                                                                               |


参考:
- StorageClassの設定など: https://cloud.google.com/kubernetes-engine/docs/how-to/persistent-volumes/gce-pd-csi-driver#create_a_storageclass

1. `StorageClass`を設定して、Claimが入ったときに生成するVolumeの設定を行う。

`pd-example-class.yaml`
```yaml
apiVersion: storage.k8s.io/v1
kind: StorageClass
metadata:
  name: pd-example
provisioner: pd.csi.storage.gke.io
volumeBindingMode: WaitForFirstConsumer
allowVolumeExpansion: true
parameters:
  type: pd-standard
reclaimPolicy: Retain
```
特に指定が無い場合はZonalStorageの設定となる。[(参考)](https://github.com/kubernetes-sigs/gcp-compute-persistent-disk-csi-driver/blob/master/docs/kubernetes/user-guides/basic.md#zonal-pd-example-for-linux-or-windows-cluster)
複数のZoneから参照したいRegionalStorageとする場合は、`replication-type`の設定が必要。[(参考)](https://github.com/kubernetes-sigs/gcp-compute-persistent-disk-csi-driver/blob/master/examples/kubernetes/demo-regional-sc.yaml)

参考価格(2021/10/03):

| Type                       | Price(per month) |
| -------------------------- | ---------------- |
| Zonal standard PD: 100 GiB | JPY 446.04       |
| Zonal balanced PD: 100 GiB | JPY 1,115.10     |
| Zonal SSD PD: 100 GiB      | JPY 1,895.67     |


ここで計算できる: https://cloud.google.com/products/calculator/

次のコマンドで設定する。これでGKEを側にStorageClassが追加される。
```bash
kubectl apply -f pd-example-class.yaml
```

2. `PersistentVolumeClaims`でVolumeを作成する。

pvc-demo.yaml
```yaml
# pvc-demo.yaml
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: pvc-demo
spec:
  storageClassName: pd-example
  accessModes:
    - ReadWriteOnce
  resources:
    requests:
      storage: 30Gi
```

次のコマンドでPersistentVolumeClaimsが作成される。
`volumeBindingMode: WaitForFirstConsumer`の設定なので、この時点ではまだVolumeは作成されていない。Pod側からマウントされることで作成される。
```bash
kubectl apply -f pvc-demo.yaml
```

## 2. Persistent volumeをPodからマウントする

sample-pod.yaml
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pd-test-pod
spec:
  containers:
  - name: cloud-sdk
    image: google/cloud-sdk:slim
    args: ["sleep","3600"]
    volumeMounts:
    - mountPath: /volume
      name: mypvc
  volumes:
  - name: mypvc
    persistentVolumeClaim:
      claimName: pvc-demo
```
本Podは、PersistentVolumeClaims: `pvc-demo`を`/volume`以下にマウントする。後ほどGCSにアクセスしたいので、gcloudコマンドが使えるイメージを使用している。

次のコマンドでPodを作成する。
```bash
kubectl apply -f sample-pod.yaml
```

## 3. GCSからのダウンロード
作成したPod内には以下のコマンドで入れる。Local環境でも問題なく入ることができた。
```bash
kubectl exec -it pd-test-pod -- /bin/bash
```

`df`コマンドを実行すると、以下のように`/volume`以下に30Gi程度のVolumeがマウントされていることが分かる。
```
root@pd-test-pod:/# df
Filesystem     1K-blocks    Used Available Use% Mounted on
overlay          5968428 4530944   1421100  77% /
tmpfs              65536       0     65536   0% /dev
tmpfs            1018124       0   1018124   0% /sys/fs/cgroup
/dev/sdb        30832548   45212  30770952   1% /volume
/dev/sda1        5968428 4530944   1421100  77% /etc/hosts
shm                65536       0     65536   0% /dev/shm
tmpfs            1018124      12   1018112   1% /run/secrets/kubernetes.io/serviceaccount
tmpfs            1018124       0   1018124   0% /proc/acpi
tmpfs            1018124       0   1018124   0% /proc/scsi
tmpfs            1018124       0   1018124   0% /sys/firmware
```

GCSバケットに保存したサンプル画像をダウンロードするには以下のコマンドを実行する。
```bash
cd /volume
gsutil cp gs://<bucket_name>/kitten.png .
```

## 4. Persistent volume準備用Podの削除
Podを削除するには以下のコマンドを実行する。
```bash
kubectl delete pod pd-test-pod
```

StorageClassにて`reclaimPolicy: Retain`と設定しているのでClaimを利用しているPodを削除してもPersistentVolumeは残る。
```bash
kubectl get pv
NAME                                       CAPACITY   ACCESS MODES   RECLAIM POLICY   STATUS   CLAIM              STORAGECLASS   REASON   AGE
pvc-e0cc4898-6a44-46a8-b4a9-14829a0db1d7   30Gi       RWO            Retain           Bound    default/pvc-demo   pd-example              126m

```

## 5. 作成したPersistent volume参照する`ReadOnlyMany`のPersistent Volume/Persistent Volume Claimsを作成
一度作成したPersistent volumeのアクセスモードを`ReadOnlyMany`に変更できない。
そこで、前ステップまでで作成したPersistentVolumeを参照するPersistentVolume作成、そのときのアクセスモードを`ReadOnlyMany`として設定する。
[(参照)](https://cloud.google.com/kubernetes-engine/docs/how-to/persistent-volumes/readonlymany-disks#csi-driver)

1. 事前に作成したPersistentVolumeのVolumeHandleを取得する

VolumeHandleは`projects/<PROJECT_ID>/zones/<ZONE_NAME>/disks/<DISK_NAME>`なので、GCPのProjectIDと設定ゾーン、DiskNameがわかっていれは設定できる。しかし、自動プロビジョニングでPersistentVolumeを作成するとDiskNameにUUIDが入るため事前に知ることができない。そこで、ここではVolumeHandleをkubectlコマンドから取得、これをYAMLファイルに設定する。下記コマンドで１番目のPersistentVolumeのVolumeHandleを取得できる。
```bash
kubectl get pv -o=jsonpath='{.items[0].spec.csi.volumeHandle}'
```

2. Apply
 
PersistentVolume/PersistentVolumeClaimを下記の通り設定する。

read-only-pd.yaml
```yaml
apiVersion: v1
kind: PersistentVolume
metadata:
  name: my-readonly-pv
spec:
  storageClassName: ""
  capacity:
    storage: 30Gi  # Set the same size as the prior set volume.
  accessModes:
    - ReadOnlyMany
  claimRef:
    namespace: default
    name: my-readonly-pvc
  csi:
    driver: pd.csi.storage.gke.io
    volumeHandle: <Set the volume handle that got from the `kubectl` command above.>
    fsType: ext4
    readOnly: true
---
apiVersion: v1
kind: PersistentVolumeClaim
metadata:
  name: my-readonly-pvc
spec:
  # Specify "" as the storageClassName so it matches the PersistentVolume's StorageClass.
  # A nil storageClassName value uses the default StorageClass. For details, see
  # https://kubernetes.io/docs/concepts/storage/persistent-volumes/#class-1
  storageClassName: ""
  accessModes:
    - ReadOnlyMany
  resources:
    requests:
      storage: 30Gi # Same volume size
```

下記コマンドでPersistentVolume/VolumeClaimを適用する。
```bash
kubectl apply -f read_only_pod.yaml
```

## 6. Persistent volume利用用Podの作成、PV内データの確認
`ReadOnlyMany`のアクセスモードせ設定したPVCを利用するPodを作成する。

read_only_pod.yaml
```yaml
apiVersion: v1
kind: Pod
metadata:
  name: pod-pvc
spec:
  containers:
  - image: k8s.gcr.io/busybox
    name: busybox
    command:
      - "sleep"
      - "3600"
    volumeMounts:
    - mountPath: /test-mnt
      name: my-volume
      readOnly: true
  volumes:
  - name: my-volume
    persistentVolumeClaim:
      claimName: my-readonly-pvc
      readOnly: true
```

下記コマンドでPodを作成する。
```bash
kubectl apply -f read-only-pd.yaml
```

作成したPodに入るには下記コマンドを実行する。
```bash
kubectl exec -it pod-pvc -- /bin/sh
```

`/test-mnt`以下にPVがマウントされるので、データを確認し、`kitten.png`が含まれていればOK。
```bash
cd test-mnt/
ls

kitten.png  lost+found
```


## 7. クリーンアップ

1. 作成したPodを削除する
```bash
kubectl delete pod pod-pvc
```

2. 作成したPVを削除する
```bash
kubectl delete pvc --all
kubectl delete pv --all
```

3. 作成したクラスタを削除する
```bash
gcloud container clusters delete $CLUSTER_NAME --zone $ZONE --quiet
```
`--quite`オプションをつけるとY/nのプロンプトがなくなる。

