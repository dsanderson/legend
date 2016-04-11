#include <iostream>
#include <vector>
#include <string>

#include "paths/path_io.h"
#include "paths/path_calc.h"

int main(int argc, char const *argv[]) {
  //Path p = import_path("paths/data/1_path.csv");
  int i1;
  int i2;
  if (argc>=3) {
    i1 = std::stoi(argv[1]);
    i2 = std::stoi(argv[2]);
  }
  else {
    std::cout << "Please provide the indicies of two paths." <<std::endl;
    return 1;
  }
  std::vector<std::string> fns = import_path_filenames("filenames.txt");
  std::vector<Path> ps = import_paths(fns);
  std::cout << "Path distance: " << path_distance(ps[i1],ps[i2])+path_distance(ps[i2],ps[i1]) << std::endl;
  optimize_path(ps[i1],ps[i2]);
  return 0;
}

//compile via g++ -Wall -g -std=c++11 -o a.out main.cpp paths/path_io.cpp paths/path_calc.cpp -lnlopt -lm
