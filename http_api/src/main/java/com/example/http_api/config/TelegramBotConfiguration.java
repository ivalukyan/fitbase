package com.example.http_api.config;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.telegram.telegrambots.meta.TelegramBotsApi;
import org.telegram.telegrambots.meta.exceptions.TelegramApiException;
import com.example.http_api.bot.TelegramBot;
import org.telegram.telegrambots.updatesreceivers.DefaultBotSession;

@Configuration
public class TelegramBotConfiguration {

    @Value("${bot.token}")
    private String botToken;

    @Value("${bot.username}")
    private String botUsername;

    @Bean
    public TelegramBotsApi telegramBotsApi() throws TelegramApiException {
        if (botToken.isEmpty() || botUsername.isEmpty()) {
            throw new IllegalArgumentException("Bot token and username can't be empty");
        }

        TelegramBotsApi telegramBotsApi = new TelegramBotsApi(DefaultBotSession.class);
        telegramBotsApi.registerBot(new TelegramBot(botToken, botUsername));
        return telegramBotsApi;
    }
}
