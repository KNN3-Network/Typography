Deploy

```commandline
    cd ai
    sudo docker build -t aicreation:latest -f content/projects/aicreation/deploy/dockerfile .
    sudo docker run -d -p 9000:9000 -v /home/centos/work/logs/aicreation:/workspace/content/projects/aicreation/logs aicreation
```