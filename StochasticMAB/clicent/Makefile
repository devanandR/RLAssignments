
CC = g++ 
COMPILE = $(CC)
#$(INCLUDES) ${FLAGS} $(LIBS)

SRC_DIR = .
DST_DIR = .

#Target
TARGET = bandit-agent

#Flags
OSFLAGS = -Dlinux
CFLAGS = -std=gnu++11 -O3 -Wall -lm
FLAGS = ${OSFLAGS} ${CFLAGS}

#Sources
SRCS =	bandit-client.cpp

#Objects
OBJS = $(SRCS:.cpp=.o)

#Rules 	

all:: 	$(TARGET) 

.cpp.o:
	$(COMPILE) $(FLAGS) -c -o $@ $(@F:%.o=%.cpp)

bandit-agent: $(OBJS)
	$(COMPILE) -o $@ $(OBJS)


clean:
	rm -f $(TARGET) $(OBJS) *~

