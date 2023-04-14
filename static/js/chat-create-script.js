let sidebar_users_div = document.querySelectorAll(".side-bar-content .users-list");
let users_block = document.querySelector(".users-block");
let sidebar_block = document.querySelector(".side-bar-content");
const logged_in_user_id = JSON.parse(document.getElementById('user_id').textContent);
let user_ids = [];

for (let user of sidebar_users_div) {
  user.addEventListener("click", () => {
    if (users_block.contains(user)) {
      users_block.removeChild(user);
      user.classList.remove("users-block-items");
      user.classList.add("users-list");
      sidebar_block.append(user);
    } else {
      user.classList.add("users-block-items");
      user.classList.remove("users-list");
      users_block.append(user);
    }
    select_ids()
  });
}

function select_ids() {
  let users = document.querySelectorAll(".users-block-items");
  let select_block = document.getElementById("id_users");
  user_ids = [];

  for (let user of users) {
    user_ids.push(parseInt(user.id));
  }

  for (let i = 0; i < select_block.options.length; i++) {
    const optionValue = parseInt(select_block.options[i].value);

    if (user_ids.includes(optionValue) || logged_in_user_id === optionValue) {
      select_block.options[i].selected = true;
    } else {
      select_block.options[i].selected = false;
    }
  }
}
