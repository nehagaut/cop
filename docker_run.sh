docker run -itd \
            -p 8080:8080 \
            -p 27017:27017 \
            -p 3000:3000 \
            -w /home/cop\
            -v the absolute path of cop project:/home/cop\
            --name cop cop 

