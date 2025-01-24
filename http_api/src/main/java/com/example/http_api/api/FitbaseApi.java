package com.example.http_api.api;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ArrayNode;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Component;

import java.io.IOException;
import java.net.URI;
import java.net.http.HttpClient;
import java.net.http.HttpRequest;
import java.net.http.HttpResponse;
import java.util.ArrayList;
import java.util.List;

@Component
public class FitbaseApi {

    private final String token;
    private final String domain;
    private final HttpClient httpClient;
    private final ObjectMapper objectMapper;
    
    public FitbaseApi(String token, String domain){
        this.token = token;
        this.domain = domain;
        this.httpClient = HttpClient.newHttpClient();
        this.objectMapper = new ObjectMapper();
    }

    private HttpRequest createRequest(String url, String method, String body){
        HttpRequest.Builder requestBuilder = HttpRequest.newBuilder()
                .uri(URI.create(url))
                .header("Club", domain)
                .header("Authorization", "Bearer " + token);
        return switch (method) {
            case "GET" -> requestBuilder.GET().build();
            case "POST" -> requestBuilder.POST(HttpRequest.BodyPublishers.ofString(body == null ? "" : body)).build();
            case "PUT" -> requestBuilder.PUT(HttpRequest.BodyPublishers.ofString(body == null ? "" : body)).build();
            case "DELETE" -> requestBuilder.DELETE().build();
            default -> throw new IllegalArgumentException("Method not supported");
        };
    }

    public List<JsonNode> getAllClients() throws IOException, InterruptedException {
        List<JsonNode> clients = new ArrayList<>();
        String url = "https://api.fitbase.io/api/v2/client";

        for (int i = 1; i<= 164; i++){
            String query = String.format("?page=%d&page_size=20", i);
            HttpRequest request = createRequest(url + query, "GET", null);
            HttpResponse<String> response = httpClient.send(request, HttpResponse.BodyHandlers.ofString());

            if (response.statusCode() == 200){
                JsonNode rootNode = objectMapper.readTree(response.body());
                ArrayNode items = (ArrayNode) rootNode.get("items");
                clients.add(items);
            } else {
                throw new IOException("Unexpected response code: " + response.statusCode());
            }
        }
        return clients;
    }
}
