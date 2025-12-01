# Detect OS
ifeq ($(OS),Windows_NT)
    EXE = .exe
    RM = del /F
else
    EXE =
    RM = rm -f
endif

# Compiler and flags
CXX = g++
CXXFLAGS = -std=c++17 -Itextgame/include -Itextgame/third_party/json-develop/single_include
LDFLAGS = -static -static-libgcc -static-libstdc++

# Source and object files
SRC = $(wildcard textgame/src/*.cpp)
OBJ = $(SRC:.cpp=.o)

# Output executable
TARGET = textgame$(EXE)

# Default build target
all: $(TARGET)

# Link object files
$(TARGET): $(OBJ)
	$(CXX) $(CXXFLAGS) $(LDFLAGS) $^ -o $@

# Compile .cpp to .o
%.o: %.cpp
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Clean build artifacts
clean:
	-@echo Cleaning up...
	-@$(RM) $(TARGET)
	-@$(RM) textgame/src/*.o

# Run the game with correct working directory
run: $(TARGET)
	@echo Running game...
	@cd textgame && ../$(TARGET)
