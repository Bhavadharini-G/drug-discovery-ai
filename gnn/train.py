import torch

def train(model, data, epochs=50):
    opt = torch.optim.Adam(model.parameters(), lr=0.01)

    for _ in range(epochs):
        opt.zero_grad()
        _, scores = model(data)
        loss = scores.pow(2).mean()
        loss.backward()
        opt.step()

    return scores.detach()
