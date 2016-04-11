#include <iostream>
#include <fstream>
#include <string>
#include <vector>
#include "path_io.h"

Path import_path(std::string filename)
{
  Path path;
  std::string line;
  std::ifstream path_file (filename);
  if(path_file.is_open())
  {
    while(std::getline(path_file,line))
    {
      if (line[0] != 'x')
      {
        Point p;
        std::string::size_type sz;     // alias of size_t
        p.x = std::stod(line,&sz);
        p.y = std::stod(line.substr(sz+1));
        path.push_back(p);
      }
    }
  }
  return path;
};

std::vector<std::string> import_path_filenames(std::string filename)
{
  std::vector<std::string> names;
  std::string line;
  std::ifstream path_file (filename);
  if(path_file.is_open())
  {
    while(std::getline(path_file,line))
    {
      names.push_back(line);
    }
  }
  return names;
};

std::vector<Path> import_paths(std::vector<std::string> path_filenames)
{
  int len = path_filenames.size();
  std::vector<Path> paths;
  for(int i=0; i<len; i++)
  {
    Path p = import_path(path_filenames[i]);
    paths.push_back(p);
  }
  return paths;
};

void print_path(Path path)
{
  int len = path.size();
  for(int i=0; i<len; i++)
  {
    std::cout << "\t" << path[i].x << ", " << path[i].y << std::endl;
  };
};

/*int main()
{
  std::cout << "Hello world" << std::endl;
  Path p = import_path("paths/data/1_path.csv");
  print_path(p);
  return 0;
};*/
