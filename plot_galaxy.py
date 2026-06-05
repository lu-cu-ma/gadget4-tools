import h5py
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde

# array of snapshot files
files = ["/home/suz/gadget4/output/G2_galaxy/snapshot_000.hdf5","/home/suz/gadget4/output/G2_galaxy/snapshot_001.hdf5","/home/suz/gadget4/output/G2_galaxy/snapshot_002.hdf5","/home/suz/gadget4/output/G2_galaxy/snapshot_003.hdf5","/home/suz/gadget4/output/G2_galaxy/snapshot_004.hdf5","/home/suz/gadget4/output/G2_galaxy/snapshot_005.hdf5","/home/suz/gadget4/output/G2_galaxy/snapshot_006.hdf5"]


i = 0 # define i to name output png files
for filepath in files:
    with h5py.File(filepath, "r") as f:
        data1 = f["PartType1/Coordinates"][:]  # type 1 particle data (dark matter)
        data2 = f["PartType2/Coordinates"][:]  # type 2 particle data (disk particles)

    # coordinates of type 1 particles (dark matter)
    x = data1[:,0]
    y = data1[:,1]
    z = data1[:,2]
    
    # coordinates of type 2 particles (disk particles)
    x2 = data2[:,0]
    y2 = data2[:,1]
    z2 = data2[:,2]

    # color by particle density
    xyz = np.vstack([x2, y2, z2])
    kde = gaussian_kde(xyz)
    density = kde(xyz)
    
    # sorting points so low-density ones are plotted first
    idx = density.argsort()
    X, Y, Z, density = x2[idx], y2[idx], z2[idx], density[idx]  # defining positions of disk particles

    # create plot
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(projection='3d')
    scatter = ax.scatter(X, Y, Z, c=density, cmap='magma', s=2, alpha=0.6)
    
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    ax.set_zlabel('Z Coordinate')
    ax.legend('type2')
    ax.set_title('G2-galaxy')
    fig.colorbar(scatter, ax=ax,label='density')


     # Save file
    #plt.savefig('00'+str(i)+'.png')

    i += 1
        
    plt.show