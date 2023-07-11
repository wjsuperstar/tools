#include <iostream>
#include <cmath>
#include <fstream>
#include <vector>
using namespace std;

const int BUFSIZE = 512;

int main(int argc, char* argv[])
{
    if (argc < 2) {
        cout << "Usage: " << argv[0] << " wav_file" << endl;
        return 1;
    }

    ifstream infile(argv[1], ios::binary | ios::in);
    if (!infile.is_open()) {
        cout << "Error opening file " << argv[1] << endl;
        return 1;
    }

    // Read the header information
    char buf[BUFSIZE];
    infile.read(buf, 44);

    // Extract the number of samples from the header
    int numSamples = *((int*)(buf + 40));

    // Allocate an array for the samples
    short* samples = new short[numSamples];

    // Read the samples into the array
    infile.read((char*)samples, numSamples * 2);
    infile.close();

    // Calculate the RMS value of the samples
    double sum = 0;
    for (int i = 0; i < numSamples; i++) {
        sum += samples[i] * samples[i];
    }
    double rms = sqrt(sum / numSamples);

    // Convert the RMS value to decibels
    double decibels = 20 * log10(rms / 32768);

    cout << "RMS value: " << rms << endl;
    cout << "Decibels: " << decibels << endl;

    delete[] samples;
    return 0;
}
