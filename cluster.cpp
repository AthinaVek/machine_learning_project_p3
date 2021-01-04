#include "help_functions.h"
#include "calculations.h"
#include "calculations_lsh.h"
#include "calculations_cluster.h"

#define m 107					//a_max < m < M/2
#define NForTable 16

using namespace std;


int main(int argc, char** argv){
	string iFile, confFile, oFile, method;
	int magic_number=0, number_of_images=0, hTableSize;
    int n_rows=0, n_cols=0, d, count=0;
    int k, L, kl, M, Ml, ky, probes, h; 
    int minc, changes = 6, first=1;
    unsigned int dist, g, min, max, x;
    double w, R;
    fNode fnode;
    bool exists;
    
	vector< vector<unsigned char> > pVec, centroids;
	vector<unsigned char> tempVec, pDim, tempC;
	vector< vector<int> > clusters, temp;
	vector< vector<int> > sVec;
	vector<int> aVec, tempIntVec, pos;
	vector< vector<distanceNode> > distRange;
	vector<distanceNode> distTemp;
	vector< vector<fNode> > fVec, cfVec;
	vector<fNode> tempfVec;
	
	srand (time(NULL));

	read_inputCluster(&argc, argv, &iFile, &iFile2, &classes, &confFile, &oFile);
	read_confFile(&k, &L, &kl, &M, &ky, confFile);

	Ml = pow(2,floor(32/kl));
	
	ifstream file (iFile);
	ofstream ofile (oFile);
	if (file.is_open()){
		read_data(file, &magic_number, &number_of_images, &n_rows, &n_cols, pVec, tempVec);

		for(int i = 0; i < k; i++){
			clusters.push_back(vector<int>());
			temp.push_back(vector<int>());
		} 
		d = n_rows * n_cols;
		hTableSize = number_of_images / NForTable;
		
		auto t1 = chrono::high_resolution_clock::now();
		
		k_means_init(centroids, number_of_images, pVec, k, d);
		
		if (ofile.is_open()){															//Lloyd's
			ofile << "Algorithm: Lloyds" << endl;

			while((count < 40) && (changes > 5)){
				changes = 0;
				lloyds_assignment(clusters, temp, number_of_images, pVec, centroids, k, d, &changes, first);
				
				if(!first){
					if (changes <= 5)
						break;
				}
				else{
					changes = 6;
				}	
				
				centroids.erase(centroids.begin(), centroids.end());                      
				update_centroids_median(centroids, pDim, pVec, clusters, tempC, k, d);    		// new centroids
				
				first = 0;
				count++;
			}
			auto t2 = chrono::high_resolution_clock::now();
			auto durationLloyds = chrono::duration_cast<chrono::microseconds>( t2 - t1 ).count();

			for(int i=0; i<k; i++){
				ofile << "CLUSTER-" << i << " {size: " << clusters[i].size() << ", centroid: [";
				for (int y=0; y<d-1; y++){
					ofile << (int)centroids[i][y] << ", ";
				}
				ofile << (int)centroids[i][d-1] << "]}" << endl;
			}

			ofile << "clustering_time: " << durationLloyds << endl;
			silhouette(clusters, centroids, pVec, k, d, ofile);
		}
		else{
			cout << "Output file does not exist." << endl;
		}
	}
	return 0;
}
