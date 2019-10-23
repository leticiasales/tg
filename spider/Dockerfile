FROM python:3.6

ENV PYTHONUNBUFFERED 1

WORKDIR /crawler

# Install essential packages
RUN apt-get update -y \
    && apt-get -y install \
        dumb-init gnupg wget ca-certificates apt-transport-https \
        ttf-wqy-zenhei unzip \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/*


# Install prerequisite packages for scrapy
RUN apt-get update -y
RUN apt-get -y install build-essential libssl-dev libffi-dev libxml2-dev libxslt-dev \
      xdg-utils lsb-release libnss3 libnspr4 libgtk-3-0 libatspi2.0-0 libatk-bridge2.0-0 \
      libasound2 libappindicator3-1 fonts-liberation

RUN pip3 install gdown

# Install Chrome Headless Browser
RUN gdown --id 1VrbzsjKkYmhuOVQ-MTrKDRfxrr85LeRH --output /chrome.deb
# RUN curl https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb -o /chrome.deb
RUN apt-get update -y
RUN dpkg -i /chrome.deb || apt-get install -yf
RUN rm /chrome.deb

# Install chromedriver
ENV CHROME_DRIVER="chromedriver_linux64"
ADD https://chromedriver.storage.googleapis.com/77.0.3865.40/chromedriver_linux64.zip .
RUN unzip $CHROME_DRIVER.zip
RUN chmod +x chromedriver
RUN mv chromedriver /usr/local/share
RUN ln -sf /usr/local/share/chromedriver /usr/local/bin
RUN rm $CHROME_DRIVER.zip

# Install requirements
COPY . /crawler
RUN pip3 install --upgrade pip
RUN pip3 install -r requirements.txt

EXPOSE 6800

CMD ["python", "crawler_job.py"]
