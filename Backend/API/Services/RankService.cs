using System;
using API.Models;

namespace API.Services
{
    public class RankService
    {
        private readonly UserService _userService;

        public RankService(UserService userService)
        {
            _userService = userService;
        }

        public User[] GetAllUserScore()
        {
            var users = _userService.Get().ToArray();

            return users;
        }
    }
}