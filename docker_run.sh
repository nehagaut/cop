docker run -itd \
            -p 8080:8080 \
            -p 27017:27017 \
            -p 3000:3000 \
            -w /home/cop\
            -v /Users/maoyiru/CMU_Y1/practicum/COP_main/cop:/home/cop\
            --name cop cop 

