import React from 'react';

class ReaderRequest extends React.Component{
    constructor(props){
        super(props)
        this.state={
            input: undefined,
            displayResponse: false,
            requestedBook: undefined,
            suggestions: undefined
        }
    }
    changeInput = event => {
        this.setState({ input: event.target.value})
    }
    handleClick = (event) => {
        let input = this.state.input.trim()
        fetch('http://127.0.0.1:5000/lms/api/book?title='+input)
            .then(res => res.json())
            .then((res) => {
                console.log(res)
                console.log(res.book[0])
                this.setState({
                  displayResponse: true,
                  requestedBook: res.book[0],
                  suggestions: res.suggestions,
                });
            }
        )
    }
    renderBook(){
        if(this.state.displayResponse){
            if (this.state.requestedBook == undefined){
                return (
                    <h1>Sorry, There is no book by that title!</h1>
                )
            }else{
                return(
                    <ul className="feed-container">
                        <li className="feed-mail-item feed-mail-header">
                            <div className="feed-book-attr">Title</div>
                            <div className="feed-book-attr">Author</div>
                            <div className="feed-book-attr">Publication</div>
                            <div className="feed-book-attr">Available Qty</div>
                        </li>
                        <li className="feed-mail-item">
                            <div className="feed-book-attr">{this.state.requestedBook.title}</div>
                            <div className="feed-book-attr">{this.state.requestedBook.authorname}</div>
                            <div className="feed-book-attr">{this.state.requestedBook.publicationname}</div>
                            <div className="feed-book-attr">{this.state.requestedBook.count}</div>
                        </li>
                    </ul>
                )    
            }
        }else{
            return null
        }
    }
    renderSuggestion(){
        if(this.state.displayResponse){
            if(this.state.suggestions.length > 0){
                return(
                    <div>
                    <h1>Other Suggestions</h1>
                    <ul className="feed-container">
                        <li className="feed-mail-item feed-mail-header">
                            <div className="feed-book-attr">Title</div>
                            <div className="feed-book-attr">Author</div>
                            <div className="feed-book-attr">Publication</div>
                        </li>
                        {
                            this.state.suggestions.map((item) => {
                                return(
                                    <li className="feed-mail-item">
                                        <div className="feed-book-attr">{item.title}</div>
                                        <div className="feed-book-attr">{item.authorname}</div>
                                        <div className="feed-book-attr">{item.publicationname}</div>
                                    </li>
                                )
                            })
                        }
                    </ul>
                    </div>
                )
            }else{
                return(
                    <h1>Sorry, You do not have any other suggestions for this book!</h1>
                )
            }
        }else{
            return null
        }
    }
    render(){
        return(
            <div>
                <div className="form-container">
                    <input placeholder="Search for a book by Title" className="userinput" onChange={(e) => this.changeInput(e)} name="mailFeed" />
                    <button className="search-btn" onClick={(e) => this.handleClick(e)}>Search</button>
                </div>
                {
                    this.renderBook()   
                }       
                {
                    this.renderSuggestion()
                }         
            </div>
        )
    }
}


export default ReaderRequest;