$(function(){


  // Todo Model
  // ----------

  var Todo = Backbone.Model.extend({
    urlRoot: '/todo_list/todos/',
    defaults: function() {  // Default attributes for the todo item.
      return {
        task: "empty todo...",
        order: Todos.nextOrder(),
        done: false
      };
    },
    toggle: function() {  // Toggle the `done` state of this todo item.
      this.save({done: !this.get("done")});
    }
  });


  // Todo Collection
  // ---------------

  var TodoList = Backbone.Collection.extend({
    url: '/todo_list/todos/',
    model: Todo,  // Reference to this collection's model.
    done: function() {  // Filter down the list of all todo items that are finished.
      return this.where({done: true});
    },
    remaining: function() {  // Filter down the list to only todo items that are still not finished.
      return this.where({done: false});
    },
    nextOrder: function() {  // We keep the Todos in sequential order, despite being saved by unordered
      if (!this.length) return 1;  // GUID in the database. This generates the next order number for new items.
      return this.last().get('order') + 1;
    },
    comparator: 'order'  // Todos are sorted by their original insertion order.
  });

  var Todos = new TodoList;  // Create our global collection of **Todos**.


  // Todo Item View
  // --------------

  var TodoView = Backbone.View.extend({  // The DOM element for a todo item...
    tagName:  "li",  //... is a list tag.
    template: _.template($('#item-template').html()),  // Cache the template function for a single item.
    events: {  // The DOM events specific to an item.
      "click .toggle"   : "toggleDone",
      "dblclick .view"  : "edit",
      "click a.destroy" : "clear",
      "keypress .edit"  : "updateOnEnter",
      "blur .edit"      : "close"
    },
    // The TodoView listens for changes to its model, re-rendering. Since there's
    // a one-to-one correspondence between a **Todo** and a **TodoView** in this
    // app, we set a direct reference on the model for convenience.
    initialize: function() {
      this.listenTo(this.model, 'change', this.render);
      this.listenTo(this.model, 'destroy', this.remove);
    },
    render: function() {  // Re-render the titles of the todo item.
      this.$el.html(this.template(this.model.toJSON()));
      this.$el.toggleClass('done', this.model.get('done'));
      this.input = this.$('.edit');
      return this;
    },
    toggleDone: function() {  // Toggle the `"done"` state of the model.
      this.model.toggle();
    },
    edit: function() {  // Switch this view into `"editing"` mode, displaying the input field.
      this.$el.addClass("editing");
      this.input.focus();
    },
    close: function() {  // Close the `"editing"` mode, saving changes to the todo.
      var value = this.input.val();
      if (!value) {
        this.clear();
      } else {
        this.model.save({task: value});
        this.$el.removeClass("editing");
      }
    },
    updateOnEnter: function(e) {  // If you hit `enter`, we're through editing the item.
      if (e.keyCode == 13) this.close();
    },
    clear: function() {  // Remove the item, destroy the model.
      this.model.destroy();
    }
  });


  // The Application
  // ---------------

  var AppView = Backbone.View.extend({  // Our overall **AppView** is the top-level piece of UI.
    el: $("#todo-app"),  // bind to the existing skeleton of the App already present in the HTML.
    statsTemplate: _.template($('#stats-template').html()),  // template for the line of statistics at the bottom of the app.
    events: {  // Delegated events for creating new items, and clearing completed ones.
      "keypress #new-todo":  "createOnEnter",
      "click #clear-completed": "clearCompleted",
      "click #toggle-all": "toggleAllComplete"
    },
    // At initialization we bind to the relevant events on the `Todos`
    // collection, when items are added or changed. Kick things off by
    // loading any preexisting todos that might be saved in *localStorage*.
    initialize: function() {  
      this.input = this.$("#new-todo");
      this.allCheckbox = this.$("#todo-toggle-all");
      this.listenTo(Todos, 'add', this.addOne);
      this.listenTo(Todos, 'reset', this.addAll);
      this.listenTo(Todos, 'all', this.render);
      this.footer = this.$('footer');
      this.main = $('#main');
      Todos.fetch();
    },
    render: function() {  // Re-rendering the App just means refreshing the statistics -- the rest of the app doesn't change.
      var done = Todos.done().length;
      var remaining = Todos.remaining().length;
      if (Todos.length) {
        this.main.show();
        this.footer.show();
        this.footer.html(this.statsTemplate({done: done, remaining: remaining}));
      } else {
        this.main.hide();
        this.footer.hide();
      }
      this.allCheckbox.checked = !remaining;
    },
    addOne: function(todo) {  // 将单个todo元素绑定一个view并添加进ul
      var view = new TodoView({model: todo});
      this.$("#todo-list").append(view.render().el);
    },
    addAll: function() {  // Add all items in the **Todos** collection at once.
      Todos.each(this.addOne, this);
    },
    createOnEnter: function(e) {  // 按下回车将添加一个新的todo model,通过model的.save持久化到服务器
      if (e.keyCode != 13) return;  // 除了回车键其他键盘键入不执行todos.create
      if (!this.input.val()) return;  // 空内容的前提下按入回车键不执行todos.create
      Todos.create({task: this.input.val()});
      this.input.val('');
    },
    // Clear all done todo items, destroying their models.
    clearCompleted: function() {
      _.invoke(Todos.done(), 'destroy');
      return false;
    },
    toggleAllComplete: function () {
      var done = this.allCheckbox.checked;
      Todos.each(function (todo) { todo.save({'done': done}); });
    }
  });
  
  var App = new AppView;
});
