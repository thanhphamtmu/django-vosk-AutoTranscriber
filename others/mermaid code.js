flowchart TB
    classDef client fill:#D8BFD8,stroke:#663399,color:#000;
    classDef app fill:#ADD8E6,stroke:#1E90FF,color:#000;
    classDef data fill:#98FB98,stroke:#228B22,color:#000;
    classDef external fill:#FFA500,stroke:#FF8C00,color:#000;

    subgraph Clients
        Browser["Web Browser (UI)"]:::client
        APIClient["REST API Client"]:::client
        WSClient["WebSocket Client"]:::client
    end

    subgraph "Application Server"
        subgraph "Django HTTP Server"
            Views["speech/views.py"]:::app
            Forms["speech/forms.py"]:::app
            URLsHTTP["speech/urls.py"]:::app
            TemplatesUpload["upload.html"]:::app
            TemplatesList["list.html"]:::app
        end
        subgraph "REST API (DRF)"
            Serializers["speech/serializers.py"]:::app
            URLsAPI["speech/urls.py"]:::app
            JWTConfig["settings.py (JWT)"]:::app
        end
        subgraph "WebSocket (Channels)"
            Consumers["speech/consumers.py"]:::app
            RoutingWS["speech/routing.py"]:::app
            ASGI["myproject/asgi.py"]:::app
        end
        Logic["speech/vosk_utils.py"]:::app
        Settings["myproject/settings.py"]:::app
        URLsProject["myproject/urls.py"]:::app
        ASGIProject["myproject/asgi.py"]:::app
        WSGI["myproject/wsgi.py"]:::app
        manage["manage.py"]:::app
        reqs["requirements.txt"]:::app
    end

    subgraph "Data Layer"
        Models["speech/models.py"]:::data
        DB["Relational Database"]:::data
        Uploads["media/uploads/"]:::data
    end

    subgraph "External Services"
        FFMPEG["FFMPEG Binary"]:::external
        VOSKModel["VOSK Model Files"]:::external
    end

    Browser -->|HTTP Upload / UI| Views
    Views -->|Validate & Save| Forms
    Forms -->|Store File| Uploads
    Views -->|Invoke| Logic
    Logic -->|Transcode| FFMPEG
    Logic -->|Recognize| VOSKModel
    Logic -->|Save Transcript| Models
    Models -->|SQL| DB
    Views -->|Trigger WS| Consumers
    Consumers -->|WS Update| WSClient
    Browser -->|WS Connect| Consumers
    APIClient -->|JWT Auth / GET| Serializers
    Serializers -->|Query| DB
    APIClient -->|Receive JSON| APIClient

    click Views "https://github.com/thanhphamtmu/django-vosk-autotranscriber/blob/main/speech/views.py"
    click Forms "https://github.com/thanhphamtmu/django-vosk-autotranscriber/blob/main/speech/forms.py"
    click URLsHTTP "https://github.com/thanhphamtmu/django-vosk-autotranscriber/blob/main/speech/urls.py"
    click TemplatesUpload "https://github.com/thanhphamtmu/django-vosk-autotranscriber/blob/main/speech/templates/upload.html"
    click TemplatesList "https://github.com/thanhphamtmu/django-vosk-autotranscriber/blob/main/speech/templates/list.html"
    click Serializers "https://github.com/thanhphamtmu/django-vosk-autotranscriber/blob/main/speech/serializers.py"
    click URLsAPI "https://github.com/thanhphamtmu/django-vosk-autotranscriber/blob/main/speech/urls.py"
    click JWTConfig "https://github.com/thanhphamtmu/django-vosk-autotranscriber/blob/main/myproject/settings.py"
    click Consumers "https://github.com/thanhphamtmu/django-vosk-autotranscriber/blob/main/speech/consumers.py"
    click RoutingWS "https://github.com/thanhphamtmu/django-vosk-autotranscriber/blob/main/speech/routing.py"
    click ASGI "https://github.com/thanhphamtmu/django-vosk-autotranscriber/blob/main/myproject/asgi.py"
    click Logic "https://github.com/thanhphamtmu/django-vosk-autotranscriber/blob/main/speech/vosk_utils.py"
    click Models "https://github.com/thanhphamtmu/django-vosk-autotranscriber/blob/main/speech/models.py"
    click Uploads "https://github.com/thanhphamtmu/django-vosk-autotranscriber/tree/main/media/uploads/"
    click manage "https://github.com/thanhphamtmu/django-vosk-autotranscriber/blob/main/manage.py"
    click reqs "https://github.com/thanhphamtmu/django-vosk-autotranscriber/blob/main/requirements.txt"
    click Settings "https://github.com/thanhphamtmu/django-vosk-autotranscriber/blob/main/myproject/settings.py"
    click URLsProject "https://github.com/thanhphamtmu/django-vosk-autotranscriber/blob/main/myproject/urls.py"
    click WSGI "https://github.com/thanhphamtmu/django-vosk-autotranscriber/blob/main/myproject/wsgi.py"
