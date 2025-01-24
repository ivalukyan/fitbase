package com.example.http_api.bot;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;
import org.telegram.telegrambots.bots.TelegramLongPollingBot;
import org.telegram.telegrambots.meta.api.methods.send.SendMessage;
import org.telegram.telegrambots.meta.api.objects.Update;
import org.telegram.telegrambots.meta.exceptions.TelegramApiException;


@Component
public class TelegramBot extends TelegramLongPollingBot {
    private static final Logger LOG = LoggerFactory.getLogger(TelegramBot.class);

    private static final String BOT_NAME = "rcbobot";
    private static final String START = "/start";
    private static final String HELP = "/help";
    private static final String ADMIN = "/admin";

    private final String botToken;

    public TelegramBot(@Value("${bot.token}") String botToken, @Value("${bot.username}") String botUsername) {
        super(botToken);
        this.botToken = botToken;
    }

    @Override
    public String getBotUsername(){
        return BOT_NAME;
    }

    @Override
    public String getBotToken(){
        return this.botToken;
    }

    @Override
    public void onUpdateReceived(Update update) {
        if (!update.hasMessage() || !update.getMessage().hasText()){
            return;
        }

        var chatId = update.getMessage().getChatId();
        var text = update.getMessage().getText();

        switch (text){
            case START:
                startCommand(chatId, update.getMessage().getChat().getUserName());
                break;
            case HELP:
                sendMessage(chatId, "Команда help");
                break;
            default:
                sendMessage(chatId, "Воспользуйтесь командой /help.");
                break;
        }

        LOG.info("Чат ID: {} Сообщение: {}", chatId, text);
    }

    private void startCommand(Long chatId, String userName){
        var text = """
                Добро пожаловать в бот, %s.
                
                Вот доступные команды:
                /start - Запуск бота.
                /help - Помощь.
                """;
        var formatedText = String.format(text, userName);
        sendMessage(chatId, formatedText);
    }

    private void sendMessage(Long chatId, String text) {
        var chatIdString = String.valueOf(chatId);
        var sendMessage = new SendMessage(chatIdString, text);
        try {
            execute(sendMessage);
        } catch (TelegramApiException e) {
            LOG.error("Ошибка отправки сообщения.", e);
        }
    }
}