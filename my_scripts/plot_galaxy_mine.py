import h5py
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import gaussian_kde


# array of snapshot files
files = ["/home/suz/gadget4/output/G2_galaxy/snapshot_000.hdf5","/home/suz/gadget4/output/G2_galaxy/snapshot_001.hdf5","/home/suz/gadget4/output/G2_galaxy/snapshot_002.hdf5","/home/suz/gadget4/output/G2_galaxy/snapshot_003.hdf5","/home/suz/gadget4/output/G2_galaxy/snapshot_004.hdf5","/home/suz/gadget4/output/G2_galaxy/snapshot_005.hdf5","/home/suz/gadget4/output/G2_galaxy/snapshot_006.hdf5"]

# for every snapshot 
for i in range(len(files)): 
    f = h5py.File(files[i],"r")
    dark_matter_part_pos = f["PartType1"]["Coordinates"][:]
    disk_star_part_pos = f["PartType2"]["Coordinates"][:]

    # Positions of dark matter particles
    x_dm= dark_matter_part_pos[:,0]
    y_dm= dark_matter_part_pos[:,1]
    z_dm= dark_matter_part_pos[:,2]

    # Positions of disk star particles
    x_disk= disk_star_part_pos[:,0]
    y_disk= disk_star_part_pos[:,1]
    z_disk= disk_star_part_pos[:,2]

    # Calculate the disk star particle density
    xyz = np.vstack([x_disk,y_disk,z_disk])   # creates a matrix (one line, one space direction position) to enables the calcul of density
    kde = gaussian_kde(xyz)         # Kernel Density Estimator: each particle is replaced by a small 3D Gaussian "blob" centered on its position. 
                                    #The KDE adds together all those blobs to create a continuous density field.
    density = kde(xyz)              #List of density of each particle 
    

    # sorting points so low-density ones are plotted first
    idx = density.argsort()

    # Associate particle position with its density
    X,Y,Z,density = x_disk[idx], y_disk[idx], z_disk[idx], density[idx]

    #plot
    fig = plt.figure(figsize=(10, 7))
    ax = fig.add_subplot(projection='3d')
    scatter = ax.scatter(X, Y, Z, c=density, cmap='magma', s=2, alpha=0.6)
    
    ax.set_xlabel('X Coordinate')
    ax.set_ylabel('Y Coordinate')
    ax.set_zlabel('Z Coordinate')
    ax.legend('type2')
    ax.set_title('G2-galaxy')
    fig.colorbar(scatter, ax=ax,label='density')

    plt.savefig('test_00'+str(i)+'.png')

    plt.show
