#include <iostream>
#include <vector>
#include <string>

#include "paths/path_io.h"
#include "paths/path_calc.h"

void help(int argc, char const *argv[]) {
  std::cout << "Please choose an option:" <<std::endl;
  std::cout << "\t--optimize [path 1] [path 2]: Find the optimal transform for path 1 to match path 2, and return the error and transform to stdout." <<std::endl;
  std::cout << "\t--transform [path 1] [tx] [ty] [rotation] [scale]: Apply the transform to the given path, return the new path to stdout." <<std::endl;
};

void optimize_score(int argc, char const *argv[]) {
  if (argc >= 4) {
    Path path_1 = import_path(argv[2]);
    Path path_2 = import_path(argv[3]);
    Transform t = optimize_path(path_1,path_2);
    std::cout << "tx:" << t.tx << std::endl;
    std::cout << "ty:" << t.ty << std::endl;
    std::cout << "rotation:" << t.rotation << std::endl;
    std::cout << "scale:" << t.scale << std::endl;
    std::cout << "score:" << t.score << std::endl;
  }
  else {
    help(argc, argv);
  }
};

void apply_transform(int argc, char const *argv[]) {
  if (argc >= 7) {
    Path path_1 = import_path(argv[2]);
    std::vector<double> t = {
      std::stod(argv[3]),
      std::stod(argv[4]),
      std::stod(argv[5]),
      std::stod(argv[6])};
    Path tp = transform_path(t, path_1);
    print_path(tp);
  }
  else {
    help(argc, argv);
  }
};

int main(int argc, char const *argv[]) {
  //Path p = import_path("paths/data/1_path.csv");
  if (argc>=2) {
    //std:string argv1 = argv[1];
    if (std::string(argv[1]) == "--optimize") {
      optimize_score(argc, argv);
    }
    else if (std::string(argv[1]) == "--transform") {
      apply_transform(argc, argv);
    }
    else {
      help(argc, argv);
    }
  }
  else {
    help(argc, argv);
  }
  return 0;
}

//compile via g++ -Wall -g -std=c++11 -o a.out main.cpp paths/path_io.cpp paths/path_calc.cpp -lnlopt -lm
